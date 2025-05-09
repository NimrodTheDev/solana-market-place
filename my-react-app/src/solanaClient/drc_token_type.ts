export type DrcToken = {
    version: "0.1.0";
    name: "drc_token";
    instructions: [
      {
        name: "createToken";
        accounts: [
          {
            name: "payer";
            isMut: true;
            isSigner: true;
          },
          {
            name: "mintAccount";
            isMut: true;
            isSigner: true;
          },
          {
            name: "metadataAccount";
            isMut: true;
            isSigner: false;
          },
          {
            name: "tokenProgram";
            isMut: false;
            isSigner: false;
          },
          {
            name: "tokenMetadataProgram";
            isMut: false;
            isSigner: false;
          },
          {
            name: "systemProgram";
            isMut: false;
            isSigner: false;
          },
          {
            name: "rent";
            isMut: false;
            isSigner: false;
          }
        ];
        args: [
          {
            name: "tokenName";
            type: "string";
          },
          {
            name: "tokenSymbol";
            type: "string";
          },
          {
            name: "tokenUri";
            type: "string";
          }
        ];
      }
    ];
    metadata: {
      address: "A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo";
    };
  };
  