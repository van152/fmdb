__int64 **__fastcall sub_140ED7A70(__int64 a1, __int64 *a2, char a3)
{
  unsigned __int64 v5; // rdx
  unsigned __int64 v6; // r12
  __int64 v7; // r15
  __int64 v8; // rbp
  __int64 v9; // rbx
  __int64 v10; // rdi
  unsigned __int64 v11; // rcx
  __int64 v12; // r8
  __int64 v13; // r14
  __int64 **result; // rax
  __int64 *v15; // rbx
  __int64 *v16; // rdx
  _QWORD *v17; // rbp
  __int64 v18; // r15
  __int64 ***v19; // rax
  __int64 v20; // r12
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // r14
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // r14
  __int64 v25; // rdi
  _QWORD *v26; // rsi
  __int64 v27; // rsi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbp
  __int64 v30; // rbp
  char v31; // [rsp+2Fh] [rbp-59h]
  __int64 v32; // [rsp+30h] [rbp-58h]
  __int64 *v33; // [rsp+38h] [rbp-50h]

  v5 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE08 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE08 + 128);
  v6 = (int)(v5 >> 3);
  v7 = *a2;
  v32 = a1;
  if ( (a2[2] - *a2) >> 3 < v6 )
  {
    if ( (v5 & 0x400000000LL) != 0 )
      sub_1400526C0(a1);
    v8 = a2[1];
    v9 = sub_1407E4490(qword_141ABD470, v5 & 0x7FFFFFFFFLL);
    sub_141758A00();
    v10 = *a2;
    if ( *a2 == 0 )
      goto LABEL_14;
    v11 = a2[2] - v10;
    if ( v11 == -1 )
    {
      v11 = *(unsigned int *)(v10 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_13;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_13;
    }
    v12 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v12) >> 3 > v11 )
    {
      v13 = *(_QWORD *)(v12 + 8 * v11);
      if ( v13 != 0 )
      {
        MEMORY[0x1419475D8](v13 + 32, v10 - *(unsigned int *)(v13 + 120));
        if ( (*(_BYTE *)(v13 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v13 + 64)) == 0)
          && *(_BYTE *)(v13 + 97) != 0 )
        {
          sub_1412D33C0(v13);
        }
        goto LABEL_14;
      }
    }
LABEL_13:
    MEMORY[0x141948990](v10 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_14:
    *a2 = v9;
    a2[1] = v9 + v8 - v7;
    a2[2] = v9 + 8 * v6;
    a1 = v32;
  }
  result = *(__int64 ***)(qword_141B5FDD0 + 128);
  v15 = *result;
  v16 = result[1];
  if ( *result != v16 )
  {
    v31 = a3;
    v33 = result[1];
    while ( 1 )
    {
      v18 = *v15;
      result = *(__int64 ***)(*v15 + 240);
      if ( result != nullptr )
      {
        if ( a3 != 0 )
        {
          if ( *(_DWORD *)(v18 + 12) == 1435 )
            v19 = (__int64 ***)(**(_QWORD **)(qword_141B5FDC8 + 128) + 32LL);
          else
            v19 = (__int64 ***)(v18 + 240);
          result = *v19;
        }
        if ( result == (__int64 **)a1 || *(_DWORD *)(a1 + 12) == 7 )
        {
          v17 = (_QWORD *)a2[1];
          if ( v17 == (_QWORD *)a2[2] )
            break;
          *v17 = v18;
          a2[1] += 8;
        }
      }
LABEL_19:
      if ( ++v15 == v16 )
        return result;
    }
    v20 = (__int64)v17 - *a2;
    v21 = v20 >> 3;
    v22 = (unsigned __int64)(v20 >> 3) >> 1;
    v23 = 0x1FFFFFFFFFFFFFFFLL - v22;
    v24 = (v20 >> 3) + v22;
    if ( v24 <= (v20 >> 3) + 1 )
      v24 = v21 + 1;
    if ( v21 > v23 )
      v24 = 0x1FFFFFFFFFFFFFFFLL;
    v25 = sub_1407E4490(qword_141ABD470, 8 * v24);
    *(_QWORD *)(v25 + v20) = v18;
    v26 = (_QWORD *)a2[1];
    sub_141758A00();
    if ( v26 != v17 )
      sub_141758A00();
    v27 = *a2;
    if ( *a2 == 0 )
    {
LABEL_46:
      *a2 = v25;
      a2[1] = v25 + 8 * ((v20 >> 3) + 1);
      result = (__int64 **)(v25 + 8 * v24);
      a2[2] = (__int64)result;
      a3 = v31;
      a1 = v32;
      v16 = v33;
      goto LABEL_19;
    }
    v28 = a2[2] - v27;
    if ( v28 == -1 )
    {
      v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_45:
        MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_46;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_45;
    }
    v29 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28 )
    {
      v30 = *(_QWORD *)(v29 + 8 * v28);
      if ( v30 != 0 )
      {
        MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
        if ( (*(_BYTE *)(v30 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) == 0)
          && *(_BYTE *)(v30 + 97) != 0 )
        {
          sub_1412D33C0(v30);
        }
        goto LABEL_46;
      }
    }
    goto LABEL_45;
  }
  return result;
}
