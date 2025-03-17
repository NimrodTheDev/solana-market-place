use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    program::{invoke, invoke_signed},
    program_error::ProgramError,
    pubkey::Pubkey,
    system_instruction,
};
use spl_token::instruction as token_instruction;

// Define the order structure
#[repr(C)]
#[derive(Debug, Default, Clone)]
pub struct MarketOrder {
    pub seller: Pubkey,
    pub token_mint: Pubkey,
    pub price: u64,
    pub amount: u64,
}

// Entry point
entrypoint!(process_instruction);

fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let instruction = instruction_data[0];

    match instruction {
        0 => create_token(accounts_iter),
        1 => list_token(accounts_iter, instruction_data),
        2 => buy_token(accounts_iter, instruction_data),
        _ => Err(ProgramError::InvalidInstructionData),
    }
}

fn create_token(accounts_iter: &mut std::slice::Iter<AccountInfo>) -> ProgramResult {
    let payer = next_account_info(accounts_iter)?;
    let mint = next_account_info(accounts_iter)?;
    let owner = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;

    invoke(
        &system_instruction::create_account(
            payer.key,
            mint.key,
            Rent::get()?.minimum_balance(spl_token::state::Mint::LEN),
            spl_token::state::Mint::LEN as u64,
            token_program.key,
        ),
        &[payer.clone(), mint.clone()],
    )?;

    msg!("Token created successfully");
    Ok(())
}

fn list_token(
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
    instruction_data: &[u8],
) -> ProgramResult {
    let seller = next_account_info(accounts_iter)?;
    let listing_account = next_account_info(accounts_iter)?;

    let order = MarketOrder {
        seller: *seller.key,
        token_mint: Pubkey::new(&instruction_data[1..33]),
        price: u64::from_le_bytes(instruction_data[33..41].try_into().unwrap()),
        amount: u64::from_le_bytes(instruction_data[41..49].try_into().unwrap()),
    };

    listing_account.try_borrow_mut_data()?[..].copy_from_slice(bytemuck::bytes_of(&order));
    msg!("Token listed successfully");
    Ok(())
}

fn buy_token(
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
    instruction_data: &[u8],
) -> ProgramResult {
    let buyer = next_account_info(accounts_iter)?;
    let seller = next_account_info(accounts_iter)?;
    let buyer_token_account = next_account_info(accounts_iter)?;
    let seller_token_account = next_account_info(accounts_iter)?;
    let token_mint = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;

    let price = u64::from_le_bytes(instruction_data[1..9].try_into().unwrap());
    let amount = u64::from_le_bytes(instruction_data[9..17].try_into().unwrap());

    invoke(
        &system_instruction::transfer(buyer.key, seller.key, price),
        &[buyer.clone(), seller.clone()],
    )?;

    invoke(
        &token_instruction::transfer(
            token_program.key,
            seller_token_account.key,
            buyer_token_account.key,
            seller.key,
            &[],
            amount,
        )?,
        &[
            seller_token_account.clone(),
            buyer_token_account.clone(),
            seller.clone(),
        ],
    )?;

    msg!("Token purchased successfully");
    Ok(())
}
