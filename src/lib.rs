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
