module whitelist::rarewave{
    use std::signer;
    use std::string::{Self, String};
    use std::vector;
    use aptos_token::token::{Self};
    use aptos_framework::account;
    use aptos_framework::coin;

    const INVALID_SIGNER: u64 = 0;
    const INVALID_AMOUNT: u64 = 1;
    const CANNOT_ZERO: u64 = 2;
    const WHITELIST_EXIST: u64 = 3;
    const WHITELIST_NOT_EXIST: u64 = 4;
    const WHIELIST_PAUSED: u64 = 5;
    const NOT_WINNER: u64 = 6;

    struct WhitelistPharse has key {
        current_phase: u64,
        whitelist: vector<Whitelist>,
    }

    struct Whitelist has store, copy {
        pharse: u64,
        royalty_payee_address: address,
        paused: bool,
        price: u64,
        end_time: u64,
        winner: vector<WhitelistWinner>,
        whitelist: vector<WhitelistEnvelope>,
    }

    struct WhitelistWinner has store, copy, drop {
        source: address,
        numNFT: u64,
    }

    struct WhitelistEnvelope has store, copy, drop {
        source: address,
        total_amount: u64
    }

    struct RareWave has key {
        collection_name: String,
        collection_description: String,
        baseuri: String,
        royalty_payee_address: address,
        royalty_points_denominator: u64,
        royalty_points_numerator: u64,
        presale_mint_time: u64,
        public_sale_mint_time: u64,
        presale_mint_price: u64,
        public_sale_mint_price: u64,
        total_supply: u64,
        minted: u64,
        token_mutate_setting:vector<bool>,
    }

    struct ResourceInfo has key {
      source: address,
      resource_cap: account::SignerCapability
    }

    fun init_module(account:&signer){
        let collection_name = string::utf8(b"Rare Wave");
        let collection_description = string::utf8(b"Rare Wave NFT");
        let baseuri = string::utf8(b"https://gateway.pinata.cloud/ipfs/QmcVxumHiLwCr9hD6VyhpRuMM17BndsE5ab6nTipMD84qG");
        let royalty_payee_address = signer::address_of(account);
        let royalty_points_denominator: u64 = 5;
        let royalty_points_numerator: u64 = 100;
        let presale_mint_time: u64 = 1667082538;
        let public_sale_mint_time: u64 = 1667082538;
        let presale_mint_price: u64 = 3;
        let public_sale_mint_price: u64 = 3;
        let total_supply: u64 = 0;
        let token_mutate_setting=vector<bool>[false, false, false, false, true];
        let collection_mutate_setting=vector<bool>[false, false, false];

        let (_resource, resource_cap) = account::create_resource_account(account, vector::empty<u8>());
        let resource_signer_from_cap = account::create_signer_with_capability(&resource_cap);

        move_to<ResourceInfo>(
            &resource_signer_from_cap,
            ResourceInfo{
                resource_cap,
                source: signer::address_of(account)
            }
        );

        let whitelist = vector::empty<Whitelist>();

        // create whitelist phase wrapper
        move_to<WhitelistPharse>(&resource_signer_from_cap, WhitelistPharse{
            current_phase: 1,
            whitelist
        });

        // create rare wave resource
        move_to<RareWave>(&resource_signer_from_cap, RareWave{
            collection_name,
            collection_description,
            baseuri,
            royalty_payee_address,
            royalty_points_denominator,
            royalty_points_numerator,
            presale_mint_time,
            public_sale_mint_time,
            presale_mint_price,
            public_sale_mint_price,
            total_supply,
            minted:0,
            token_mutate_setting
        });

        // create collection
        token::create_collection(
            &resource_signer_from_cap, 
            collection_name, 
            collection_description, 
            baseuri, 
            0,
            collection_mutate_setting
        );
    }

    // get whitelist info
    public entry fun get_whitelist_info(
        resource_addr: address,
        pharse: u64
    ) : (bool, u64, bool, u64, u64, vector<WhitelistWinner>, vector<WhitelistEnvelope>) acquires WhitelistPharse {
        // get whitelist pharse from resource address
        let whitelist_pharse = borrow_global_mut<WhitelistPharse>(resource_addr);
        let i = 0;
        let len = vector::length<Whitelist>(&whitelist_pharse.whitelist);

        // loop over whitelist and get the whitelist info by pharse
        while (i < len) {
            let whitelist = vector::borrow<Whitelist>(&whitelist_pharse.whitelist, i);
            if (whitelist.pharse == pharse) {
                return (
                    true,
                    whitelist.pharse,
                    whitelist.paused,
                    whitelist.price,
                    whitelist.end_time,
                    whitelist.winner,
                    whitelist.whitelist
                )
            };
            i = i + 1;
        };

        return (false, 0, false, 0, 0, vector::empty<WhitelistWinner>(), vector::empty<WhitelistEnvelope>())
    }

    // create whitelist
    public entry fun create_whitelist(
        account: &signer,
        resource_addr:address,
        royalty_payee_address: address,
        paused: bool,
        price: u64,
        end_time: u64,
    ) acquires ResourceInfo, WhitelistPharse {
        // get signer address
        let account_addr = signer::address_of(account);

        // check signer is admin
        let resource_data = borrow_global<ResourceInfo>(resource_addr);
        assert!(resource_data.source == account_addr, INVALID_SIGNER);

        // get whitelist pharse
        let whitelist_phase = borrow_global_mut<WhitelistPharse>(resource_addr);
        whitelist_phase.current_phase = whitelist_phase.current_phase + 1;

        let whitelist = vector::empty<WhitelistEnvelope>();
        let winner = vector::empty<WhitelistWinner>();

        // push back new whitelist to whitelist wrapper
        vector::push_back(&mut whitelist_phase.whitelist, Whitelist {
            pharse: whitelist_phase.current_phase,
            royalty_payee_address,
            paused,
            price,
            end_time,
            whitelist,
            winner,
        });
    }

    public entry fun join_whitelist(
        joiner: &signer,
        resource_addr: address,
    ) acquires WhitelistPharse {
        let whitelist_phase = borrow_global_mut<WhitelistPharse>(resource_addr);
        let whitelist = vector::borrow_mut<Whitelist>(&mut whitelist_phase.whitelist, whitelist_phase.current_phase - 1);
        assert!(whitelist.paused == false, WHIELIST_PAUSED);
        let now = aptos_framework::timestamp::now_seconds();
        assert!(now < whitelist.end_time, WHIELIST_PAUSED);

        let joiner_addr = signer::address_of(joiner);

        // get joiner whitelist envelope
        let (success, joiner_whitelist_envelope) = get_whitelist_envelope_by_address(whitelist, joiner_addr);

        // create whitelist envelope for user when user join whitelist in first time
        if (!success) {
            let whitelist_envelope = WhitelistEnvelope {
                source: joiner_addr,
                total_amount: 1
            };
            vector::push_back(&mut whitelist.whitelist, whitelist_envelope);
        } else {
            // update whitelist envelope for user when user join whitelist in second time
            joiner_whitelist_envelope.total_amount = joiner_whitelist_envelope.total_amount + 1;
        };

        coin::transfer<0x1::aptos_coin::AptosCoin>(joiner, resource_addr, whitelist.price);
    }

    public entry fun claim_nft(
        joiner: &signer,
        resource_addr: address,
    ) acquires WhitelistPharse, ResourceInfo, RareWave {
        let joiner_addr = signer::address_of(joiner);

        // check joiner is winner in whitelist
        let whitelist_phase = borrow_global<WhitelistPharse>(resource_addr);
        let whitelist = vector::borrow<Whitelist>(&whitelist_phase.whitelist, whitelist_phase.current_phase - 1);
        let (is_winer, winner_info) = check_is_winner(whitelist, joiner_addr);
        let i = 0;
        assert!(is_winer, NOT_WINNER);

        // get resource signer
        let resource_data = borrow_global<ResourceInfo>(resource_addr);
        let resource_signer_from_cap = account::create_signer_with_capability(&resource_data.resource_cap);

        // get collection data
        let collection_data = borrow_global_mut<RareWave>(resource_addr);
        let baseuri = collection_data.baseuri;
        let properties = vector::empty<String>();

        while (i < winner_info.numNFT) {
            let owl = collection_data.minted;
            let token_name = collection_data.collection_name;
            string::append(&mut token_name,string::utf8(b" #"));
            string::append(&mut token_name,num_str(owl));
            string::append(&mut baseuri,string::utf8(b".json"));

            token::create_token_script(
                &resource_signer_from_cap,
                collection_data.collection_name,
                token_name,
                collection_data.collection_description,
                1,
                0,
                baseuri,
                collection_data.royalty_payee_address,
                collection_data.royalty_points_denominator,
                collection_data.royalty_points_numerator,
                collection_data.token_mutate_setting,
                properties,
                vector<vector<u8>>[],
                properties
            );

            let token_data_id = token::create_token_data_id(resource_addr,collection_data.collection_name,token_name);
            token::opt_in_direct_transfer(joiner,true);

            token::mint_token_to(&resource_signer_from_cap, joiner_addr , token_data_id,1);
            collection_data.minted=collection_data.minted+1;

            i = i + 1;
        };

    }

    fun check_is_winner(whitelist: &Whitelist, joiner_addr: address): (bool,& WhitelistWinner) {
        let i = 0;
        let len = vector::length<WhitelistWinner>(&whitelist.winner);
        while (i < len) {
            let winner = vector::borrow<WhitelistWinner>(&whitelist.winner, i);
            if (winner.source == joiner_addr) {
                return (true, winner)
            };
            i = i + 1;
        };

        return (false, vector::borrow<WhitelistWinner>(&whitelist.winner, 0))
    }

    public entry fun update_winner(
        account: &signer,
        resource_addr: address,
        pharse: u64,
        winner: vector<WhitelistWinner>
    ) acquires ResourceInfo, WhitelistPharse {
        // get signer address
        let account_addr = signer::address_of(account);

        // check signer is admin
        let resource_data = borrow_global<ResourceInfo>(resource_addr);
        assert!(resource_data.source == account_addr, INVALID_SIGNER);

        // check whitelist phase is alrealdy exist
        let (exist, _, _, _, _, _, _) = get_whitelist_info(resource_addr, pharse);
        assert!(exist, WHITELIST_NOT_EXIST);

        // get whitelist pharse
        let whitelist_phase = borrow_global_mut<WhitelistPharse>(resource_addr);

        // loop over whitelist and get the whitelist info by pharse
        let i = 0;
        let len = vector::length<Whitelist>(&whitelist_phase.whitelist);
        while (i < len) {
            let whitelist = vector::borrow_mut<Whitelist>(&mut whitelist_phase.whitelist, i);
            if (whitelist.pharse == pharse) {
                vector::append(&mut whitelist.winner, winner);
                return
            };
            i = i + 1;
        };
    }

    fun get_whitelist_envelope_by_address(
        whitelist: &mut Whitelist,
        joiner_addr: address
    ) : (bool,&mut WhitelistEnvelope)  {
        let i = 0;
        let len = vector::length<WhitelistEnvelope>(&whitelist.whitelist);
        while (i < len) {
            let whitelist_envelope = vector::borrow_mut<WhitelistEnvelope>(&mut whitelist.whitelist, i);
            if (whitelist_envelope.source == joiner_addr) {
                return (true,whitelist_envelope)
            };
            i = i + 1;
        };

        return (false, vector::borrow_mut<WhitelistEnvelope>(&mut whitelist.whitelist, 0))
    }

    fun num_str(num: u64): String{
        let v1 = vector::empty();
        while (num/10 > 0){
            let rem = num%10;
            vector::push_back(&mut v1, (rem+48 as u8));
            num = num/10;
        };
        vector::push_back(&mut v1, (num+48 as u8));
        vector::reverse(&mut v1);
        string::utf8(v1)
    }
}