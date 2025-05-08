use borsh::BorshSerialize;
use solana_program::account_info::next_account_info;
use solana_program::entrypoint;
use solana_program::entrypoint::ProgramResult;
use solana_program::{account_info::AccountInfo, program::invoke_signed, pubkey::Pubkey};
use spl_token::instruction::initialize_mint;

// By using a generic lifetime 'a for all AccountInfo references,
// we tell Rust that all these parameters have the same lifetime
fn create_token_mint<'a>(
    token_mint: &'a AccountInfo<'a>,
    rent_sysvar: &'a AccountInfo<'a>,
    token_program: &'a AccountInfo<'a>,
    authority: &Pubkey,
    decimals: u8,
    signer_seeds: &[&[u8]],
) -> ProgramResult {
    let ix = initialize_mint(token_program.key, token_mint.key, authority, None, decimals)?;

    invoke_signed(
        &ix,
        &[
            token_mint.clone(),
            rent_sysvar.clone(),
            token_program.clone(),
        ],
        &[signer_seeds],
    )?;

    Ok(())
}

entrypoint!(process_instruction);
pub fn process_instruction<'a>(
    program_id: &Pubkey,
    accounts: &'a [AccountInfo<'a>],
    instruction_data: &'a [u8],
) -> ProgramResult {
    let account_info_iter = &mut accounts.iter();
    let token_mint = next_account_info(account_info_iter)?;
    let rent_sysvar = next_account_info(account_info_iter)?;
    let token_program = next_account_info(account_info_iter)?;
    let authority = next_account_info(account_info_iter)?;
    let signer_seeds: &[&[u8]] = &[];
    // Static values for this simple test
    let decimals = 6;
    create_token_mint(
        token_mint,
        rent_sysvar,
        token_program,
        authority.key,
        decimals,
        signer_seeds,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use borsh::BorshSerialize;
    use solana_program::account_info::next_account_info;
    use solana_program::instruction::AccountMeta;
    use solana_program::program_pack::Pack;
    use solana_program::rent::Rent;
    use solana_program_test::*;
    use solana_sdk::serde_varint::serialize;
    use solana_sdk::{
        account::Account,
        instruction::Instruction,
        pubkey::Pubkey,
        signature::{Keypair, Signer},
        system_instruction, sysvar,
        transaction::Transaction,
    };
    use spl_token::state::Mint;

    #[tokio::test]
    async fn test_create_token_mint() {
        let program_id = Pubkey::new_unique();
        let mint_keypair = Keypair::new();
        let authority = Keypair::new();

        let mut program_test = ProgramTest::new(
            "my_solana_program", // name in Cargo.toml
            program_id,
            None,
        );

        // Add token mint account to be created
        program_test.add_account(
            mint_keypair.pubkey(),
            Account {
                lamports: 1_000_000_000, // Enough for rent
                data: vec![0u8; Mint::LEN],
                owner: spl_token::id(),
                executable: false,
                rent_epoch: 0,
            },
        );

        // Add the rent sysvar manually
        program_test.add_account(
            sysvar::rent::id(),
            Account {
                lamports: 0,
                data: vec![0u8; Mint::LEN],
                owner: solana_sdk::sysvar::id(),
                executable: false,
                rent_epoch: 0,
            },
        );

        let (mut banks_client, payer, recent_blockhash) = program_test.start().await;

        let instruction = Instruction::new_with_bincode::<[u8; 0]>(
            program_id,
            &[] as &[u8; 0], // No custom instruction data
            vec![
                AccountMeta::new(mint_keypair.pubkey(), false),
                AccountMeta::new_readonly(sysvar::rent::id(), false),
                AccountMeta::new_readonly(spl_token::id(), false),
                AccountMeta::new_readonly(authority.pubkey(), false),
            ],
        );

        let tx = Transaction::new_signed_with_payer(
            &[instruction],
            Some(&payer.pubkey()),
            &[&payer, &mint_keypair, &authority],
            recent_blockhash,
        );

        let result = banks_client.process_transaction(tx).await;
        assert!(result.is_ok());

        // Fetch and verify the token mint account
        let mint_account = banks_client
            .get_account(mint_keypair.pubkey())
            .await
            .unwrap()
            .unwrap();

        let mint_data = Mint::unpack(&mint_account.data).unwrap();
        assert_eq!(mint_data.decimals, 6);
        assert_eq!(mint_data.mint_authority.unwrap(), authority.pubkey());
    }
}
