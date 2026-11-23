__int64 __fastcall sub_141567CA0(_QWORD *a1, int a2, _QWORD *a3)
{
  unsigned __int64 v5; // r13
  unsigned __int64 v6; // rbx
  char v7; // r15
  __int64 v8; // r12
  __int64 v9; // rcx
  unsigned __int64 v10; // rbp
  unsigned __int64 v11; // rdi
  __int16 v12; // r14
  __int64 v13; // rcx
  unsigned __int64 v14; // rbp
  unsigned __int64 v15; // r15
  unsigned __int64 v16; // rdi
  __int64 v17; // rcx
  __int64 v18; // rax
  unsigned __int64 v19; // rax
  unsigned __int64 v20; // rax
  __int64 v21; // rbx
  unsigned __int64 v22; // r14
  __int64 v23; // rdi
  unsigned __int64 v24; // rcx
  bool v25; // al
  unsigned __int64 v26; // r12
  __int64 v27; // rdi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbp
  __int64 v30; // rbp
  bool v31; // al
  _BYTE v33[72]; // [rsp+20h] [rbp-48h] BYREF

  v5 = 0;
  LODWORD(v6) = 0;
  if ( a2 <= 1886679856 )
  {
    if ( a2 != 1734438193 )
    {
      if ( a2 == 1734438194 )
      {
        v5 = 1;
      }
      else
      {
        if ( a2 != 1734438195 )
          return (unsigned int)v6;
        v5 = 2;
      }
    }
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
    {
      v7 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      v8 = a1[8];
      v9 = a1[9];
      v6 = v9 - v8;
      if ( v9 - v8 <= v5 )
      {
        v10 = v5 + 1;
        v11 = v5 + 1 - v6;
        if ( v5 + 1 >= v6 )
        {
          v19 = a1[10] - v8;
          if ( v19 <= v5 )
          {
            v22 = v19 + (v19 >> 1);
            if ( v22 <= v10 )
              v22 = v5 + 1;
            v8 = sub_1407E4490(qword_141ABD470, v22);
            v6 += v8;
            sub_141758A10(v6, 0, v11);
            sub_141758A00(v8, a1[8], a1[9] - a1[8]);
            v23 = a1[8];
            if ( v23 != 0 )
            {
              v24 = a1[10] - v23;
              if ( v24 == -1 )
                v24 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v6 = *(_QWORD *)(qword_141ABD470 + 24), (__int64)(*(_QWORD *)(qword_141ABD470 + 32) - v6) >> 3 > v24)
                && (v6 = *(_QWORD *)(v6 + 8 * v24)) != 0 )
              {
                MEMORY[0x1419475D8](v6 + 32, v23 - *(unsigned int *)(v6 + 120));
                v25 = *(_BYTE *)(v6 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 + 64)) != 0;
                if ( !v25 && *(_BYTE *)(v6 + 97) != 0 )
                  sub_1412D33C0(v6);
              }
              else
              {
                MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            a1[8] = v8;
            a1[9] = v8 + v10;
            a1[10] = v8 + v22;
          }
          else
          {
            v6 = v9 + v11;
            sub_141758A10(v9, 0, v11);
            a1[9] = v6;
            v8 = a1[8];
          }
        }
        else
        {
          a1[9] = v8 + 1;
        }
      }
      *(_BYTE *)(v8 + v5) = v7;
      goto LABEL_55;
    }
    goto LABEL_21;
  }
  if ( a2 <= 1886679858 )
  {
    v5 = a2 != 1886679857;
    goto LABEL_17;
  }
  if ( a2 == 1886679859 )
  {
    v5 = 2;
LABEL_17:
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
    {
      v12 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      v6 = a1[5];
      v13 = a1[6];
      v14 = (__int64)(v13 - v6) >> 1;
      if ( v14 <= v5 )
      {
        v15 = v5 + 1;
        v16 = v5 + 1 - v14;
        if ( v5 + 1 >= v14 )
        {
          v20 = (__int64)(a1[7] - v6) >> 1;
          if ( v20 <= v5 )
          {
            v26 = v20 + (v20 >> 1);
            if ( v26 <= v15 )
              v26 = v5 + 1;
            v6 = sub_1407E4490(qword_141ABD470, 2 * v26);
            sub_141758A10(v6 + 2 * v14, 0, 2 * v16);
            sub_141758A00(v6, a1[5], a1[6] - a1[5]);
            v27 = a1[5];
            if ( v27 != 0 )
            {
              v28 = a1[7] - v27;
              if ( v28 == -1 )
                v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v29 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28)
                && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
              {
                MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
                v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
                if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
                  sub_1412D33C0(v30);
              }
              else
              {
                MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            a1[5] = v6;
            a1[6] = v6 + 2 * v15;
            a1[7] = v6 + 2 * v26;
          }
          else
          {
            v21 = v13 + 2 * v16;
            sub_141758A10(v13, 0, 2 * v16);
            a1[6] = v21;
            v6 = a1[5];
          }
        }
        else
        {
          a1[6] = v6 + 2;
        }
      }
      *(_WORD *)(v6 + 2 * v5) = v12;
      goto LABEL_55;
    }
LABEL_21:
    v17 = a1[8];
    if ( a1[9] - v17 > v5 )
    {
      sub_141758A00(v5 + v17, v17 + v5 + 1, a1[9] - (v17 + v5 + 1));
      --a1[9];
    }
    v18 = a1[5];
    LOBYTE(v6) = 1;
    if ( (a1[6] - v18) >> 1 > v5 )
    {
      sub_141758A00(v18 + 2 * v5, v18 + 2 * v5 + 2, a1[6] - (v18 + 2 * v5 + 2));
      a1[6] -= 2LL;
    }
    return (unsigned int)v6;
  }
  if ( a2 == 1952801133 )
  {
    v6 = qword_141B5FE40;
    sub_140FE7960(v33, a3, 1416914273);
    a1[3] = sub_140FA3700(v6, v33);
LABEL_55:
    LOBYTE(v6) = 1;
  }
  return (unsigned int)v6;
}
