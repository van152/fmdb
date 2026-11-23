char __fastcall sub_140FAD900(_QWORD *a1)
{
  __int64 v2; // rdi
  unsigned __int64 v3; // rcx
  __int64 v4; // rbx
  __int64 v5; // rbx
  signed __int32 v6; // et0
  char result; // al
  __int64 *v8; // r15
  __int64 *v9; // rdi
  __int64 *v10; // rbx
  __int64 v11; // rsi
  __int64 v12; // rcx
  __int64 v13; // rsi
  unsigned __int64 v14; // rcx
  __int64 v15; // rdx
  __int64 v16; // rbx
  signed __int32 v17; // et0
  __int64 v18; // rdi
  unsigned __int64 v19; // rcx
  __int64 v20; // rbx
  __int64 v21; // rbx
  signed __int32 v22; // et0
  __int64 v23; // rdi
  unsigned __int64 v24; // rcx
  __int64 v25; // rbx
  __int64 v26; // rbx
  signed __int32 v27; // et0
  __int64 v28; // rdi
  unsigned __int64 v29; // rcx
  __int64 v30; // rbx
  __int64 v31; // rbx
  signed __int32 v32; // et0
  __int64 v33; // rdi
  unsigned __int64 v34; // rcx
  __int64 v35; // rbx
  __int64 v36; // rbx
  signed __int32 v37; // et0
  __int64 v38; // rdi
  unsigned __int64 v39; // rcx
  __int64 v40; // rbx
  __int64 v41; // rbx
  signed __int32 v42; // et0
  __int64 v43; // rcx
  __int64 v44; // rcx
  __int64 v45; // rcx

  v2 = a1[27];
  if ( v2 != 0 )
  {
    v3 = a1[29] - v2;
    if ( v3 == -1 )
      v3 = *(unsigned int *)(v2 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v4 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v4) >> 3 > v3 )
      {
        v5 = *(_QWORD *)(v4 + 8 * v3);
        if ( v5 != 0 )
        {
          MEMORY[0x1419475D8](v5 + 32, v2 - *(unsigned int *)(v5 + 120));
          if ( *(_BYTE *)(v5 + 72) != 0 )
          {
            v6 = _InterlockedDecrement((volatile signed __int32 *)(v5 + 64));
            result = v6 != 0;
            if ( v6 != 0 )
              goto LABEL_11;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v5 + 97) != 0 )
            result = sub_1412D33C0(v5);
          goto LABEL_11;
        }
      }
    }
    result = MEMORY[0x141948990](v2 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_11:
    a1[29] = 0;
    a1[28] = 0;
    a1[27] = 0;
  }
  v8 = (__int64 *)a1[21];
  v9 = (__int64 *)a1[22];
  if ( v8 != v9 )
  {
    v10 = (__int64 *)a1[21];
    do
    {
      v11 = *v10;
      if ( *v10 != 0 )
      {
        v12 = *(_QWORD *)(v11 + 8);
        if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 - 4)) == 0 )
          sub_1412EC9A0(v12 - 4);
        sub_140FC6370(v11);
      }
      ++v10;
    }
    while ( v10 != v9 );
    v13 = a1[22] - (_QWORD)v9;
    result = sub_141758A00();
    a1[22] = (char *)v8 + v13;
    v9 = (__int64 *)a1[21];
  }
  if ( v9 != nullptr )
  {
    v14 = a1[23] - (_QWORD)v9;
    if ( v14 == -1 )
      v14 = *(unsigned int *)((char *)v9 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v15 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 > v14 )
      {
        v16 = *(_QWORD *)(v15 + 8 * v14);
        if ( v16 != 0 )
        {
          MEMORY[0x1419475D8](v16 + 32, (char *)v9 - *(unsigned int *)(v16 + 120));
          if ( *(_BYTE *)(v16 + 72) != 0 )
          {
            v17 = _InterlockedDecrement((volatile signed __int32 *)(v16 + 64));
            result = v17 != 0;
            if ( v17 != 0 )
              goto LABEL_31;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v16 + 97) != 0 )
            result = sub_1412D33C0(v16);
          goto LABEL_31;
        }
      }
    }
    result = MEMORY[0x141948990]((char *)v9 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_31:
    a1[23] = 0;
    a1[22] = 0;
    a1[21] = 0;
  }
  v18 = a1[18];
  if ( v18 == 0 )
    goto LABEL_43;
  v19 = a1[20] - v18;
  if ( v19 == -1 )
    v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
  {
    v20 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19 )
    {
      v21 = *(_QWORD *)(v20 + 8 * v19);
      if ( v21 != 0 )
      {
        MEMORY[0x1419475D8](v21 + 32, v18 - *(unsigned int *)(v21 + 120));
        if ( *(_BYTE *)(v21 + 72) != 0 )
        {
          v22 = _InterlockedDecrement((volatile signed __int32 *)(v21 + 64));
          result = v22 != 0;
          if ( v22 != 0 )
            goto LABEL_42;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v21 + 97) != 0 )
          result = sub_1412D33C0(v21);
        goto LABEL_42;
      }
    }
  }
  result = MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_42:
  a1[20] = 0;
  a1[19] = 0;
  a1[18] = 0;
LABEL_43:
  v23 = a1[15];
  if ( v23 == 0 )
    goto LABEL_54;
  v24 = a1[17] - v23;
  if ( v24 == -1 )
    v24 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
  {
    v25 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v25) >> 3 > v24 )
    {
      v26 = *(_QWORD *)(v25 + 8 * v24);
      if ( v26 != 0 )
      {
        MEMORY[0x1419475D8](v26 + 32, v23 - *(unsigned int *)(v26 + 120));
        if ( *(_BYTE *)(v26 + 72) != 0 )
        {
          v27 = _InterlockedDecrement((volatile signed __int32 *)(v26 + 64));
          result = v27 != 0;
          if ( v27 != 0 )
            goto LABEL_53;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v26 + 97) != 0 )
          result = sub_1412D33C0(v26);
        goto LABEL_53;
      }
    }
  }
  result = MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_53:
  a1[17] = 0;
  a1[16] = 0;
  a1[15] = 0;
LABEL_54:
  v28 = a1[12];
  if ( v28 == 0 )
    goto LABEL_65;
  v29 = a1[14] - v28;
  if ( v29 == -1 )
    v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
  {
    v30 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
    {
      v31 = *(_QWORD *)(v30 + 8 * v29);
      if ( v31 != 0 )
      {
        MEMORY[0x1419475D8](v31 + 32, v28 - *(unsigned int *)(v31 + 120));
        if ( *(_BYTE *)(v31 + 72) != 0 )
        {
          v32 = _InterlockedDecrement((volatile signed __int32 *)(v31 + 64));
          result = v32 != 0;
          if ( v32 != 0 )
            goto LABEL_64;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v31 + 97) != 0 )
          result = sub_1412D33C0(v31);
        goto LABEL_64;
      }
    }
  }
  result = MEMORY[0x141948990](v28 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_64:
  a1[14] = 0;
  a1[13] = 0;
  a1[12] = 0;
LABEL_65:
  v33 = a1[9];
  if ( v33 == 0 )
    goto LABEL_76;
  v34 = a1[11] - v33;
  if ( v34 == -1 )
    v34 = *(unsigned int *)(v33 - *(unsigned int *)(qword_141ABD470 + 48));
  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
  {
    v35 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34 )
    {
      v36 = *(_QWORD *)(v35 + 8 * v34);
      if ( v36 != 0 )
      {
        MEMORY[0x1419475D8](v36 + 32, v33 - *(unsigned int *)(v36 + 120));
        if ( *(_BYTE *)(v36 + 72) != 0 )
        {
          v37 = _InterlockedDecrement((volatile signed __int32 *)(v36 + 64));
          result = v37 != 0;
          if ( v37 != 0 )
            goto LABEL_75;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v36 + 97) != 0 )
          result = sub_1412D33C0(v36);
        goto LABEL_75;
      }
    }
  }
  result = MEMORY[0x141948990](v33 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_75:
  a1[11] = 0;
  a1[10] = 0;
  a1[9] = 0;
LABEL_76:
  v38 = a1[6];
  if ( v38 != 0 )
  {
    v39 = a1[8] - v38;
    if ( v39 == -1 )
      v39 = *(unsigned int *)(v38 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v40 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v40) >> 3 > v39 )
      {
        v41 = *(_QWORD *)(v40 + 8 * v39);
        if ( v41 != 0 )
        {
          MEMORY[0x1419475D8](v41 + 32, v38 - *(unsigned int *)(v41 + 120));
          if ( *(_BYTE *)(v41 + 72) != 0 )
          {
            v42 = _InterlockedDecrement((volatile signed __int32 *)(v41 + 64));
            result = v42 != 0;
            if ( v42 != 0 )
              goto LABEL_86;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v41 + 97) != 0 )
            result = sub_1412D33C0(v41);
          goto LABEL_86;
        }
      }
    }
    result = MEMORY[0x141948990](v38 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_86:
    a1[8] = 0;
    a1[7] = 0;
    a1[6] = 0;
  }
  v43 = a1[5];
  if ( v43 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43 - 4)) == 0 )
    result = sub_1412EC9A0(v43 - 4);
  v44 = a1[4];
  if ( v44 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v44 - 4)) == 0 )
    result = sub_1412EC9A0(v44 - 4);
  v45 = a1[3];
  if ( v45 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v45 - 4)) == 0 )
    return sub_1412EC9A0(v45 - 4);
  return result;
}
