_DWORD *__fastcall sub_141727D70(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // rbp
  unsigned int v6; // esi
  __int64 v7; // r15
  __int64 v8; // rbx
  __int64 v9; // rsi
  __int64 v10; // r12
  __int64 v11; // rdi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // r15
  __int64 v17; // rax
  _QWORD *v18; // rbx
  __int64 v19; // rbp
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // r12
  unsigned __int64 v22; // rsi
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rdi
  _QWORD *v27; // r14
  __int64 v28; // rbx
  unsigned __int64 v29; // rcx
  __int64 v30; // rbp
  __int64 v31; // rbp
  unsigned int v33; // [rsp+24h] [rbp-74h] BYREF
  _QWORD v34[4]; // [rsp+28h] [rbp-70h] BYREF
  _DWORD *v35; // [rsp+48h] [rbp-50h]
  _QWORD *v36; // [rsp+50h] [rbp-48h]

  v4 = a2;
  v33 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v33, a3: 4);
  v6 = v33;
  if ( qword_141AA7808 <= (unsigned __int64)v33 )
  {
LABEL_43:
    *a1 = 1;
    return a1;
  }
  v35 = a1;
  v7 = *a3;
  if ( (a3[2] - *a3) >> 5 < (unsigned __int64)v33 )
  {
    v8 = a3[1];
    v9 = 32LL * v33;
    v10 = sub_1407E4490(a1: qword_141ABD470, a2: v9);
    sub_141758A00(a1: v10, a2: *a3, a3: a3[1] - *a3);
    v11 = *a3;
    if ( *a3 == 0 )
    {
LABEL_13:
      *a3 = v10;
      a3[1] = v10 + v8 - v7;
      a3[2] = v10 + v9;
      v6 = v33;
      goto LABEL_14;
    }
    v12 = a3[2] - v11;
    if ( v12 == -1 )
    {
      v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
        if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
          sub_1412D33C0(a1: v14);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( v6 != 0 )
  {
    v16 = 0;
    v36 = v4;
    while ( 1 )
    {
      v34[3] = 0xFFFF00000000LL;
      v34[2] = 0xFFFFFFFF00000000uLL;
      LODWORD(v34[0]) = 124518401;
      *(_QWORD *)((char *)&v34[1] + 1) = -1;
      *(_QWORD *)((char *)v34 + 4) = -1;
      if ( (unsigned __int8)sub_14156ADD0(a1: v34, a2: v4) == 0 )
      {
        a1 = v35;
        goto LABEL_43;
      }
      if ( *(_DWORD *)(*v4 + 16LL) != 0 )
        goto LABEL_41;
      v18 = (_QWORD *)a3[1];
      if ( v18 == (_QWORD *)a3[2] )
        break;
      v18[3] = v34[3];
      v18[2] = v34[2];
      v17 = v34[0];
      v18[1] = v34[1];
      *v18 = v17;
      a3[1] += 32;
LABEL_17:
      if ( ++v16 >= (unsigned __int64)v33 )
        goto LABEL_41;
    }
    v19 = (__int64)v18 - *a3;
    v20 = v19 >> 5;
    v21 = (v19 >> 5) + 1;
    v22 = (unsigned __int64)(v19 >> 5) >> 1;
    v23 = 0x7FFFFFFFFFFFFFFLL - v22;
    v24 = (v19 >> 5) + v22;
    if ( v24 <= v21 )
      v24 = v20 + 1;
    if ( v20 > v23 )
      v24 = 0x7FFFFFFFFFFFFFFLL;
    v25 = 32 * v24;
    v26 = sub_1407E4490(a1: qword_141ABD470, a2: v25);
    qmemcpy((void *)(v26 + v19), v34, 32);
    v27 = (_QWORD *)a3[1];
    sub_141758A00(a1: v26, a2: *a3, a3: (char *)v18 - *a3);
    if ( v27 != v18 )
      sub_141758A00(a1: v26 + v19 + 32, a2: v18, a3: a3[1] - (_QWORD)v18);
    v28 = *a3;
    if ( *a3 == 0 )
    {
LABEL_38:
      *a3 = v26;
      a3[1] = v26 + 32 * v21;
      a3[2] = v26 + v25;
      v4 = v36;
      goto LABEL_17;
    }
    v29 = a3[2] - v28;
    if ( v29 == -1 )
    {
      v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_37:
        MEMORY[0x141948990](a1: v28 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_38;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_37;
    }
    v30 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
    {
      v31 = *(_QWORD *)(v30 + 8 * v29);
      if ( v31 != 0 )
      {
        MEMORY[0x1419475D8](a1: v31 + 32, a2: v28 - *(unsigned int *)(v31 + 120));
        if ( (*(_BYTE *)(v31 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) == 0)
          && *(_BYTE *)(v31 + 97) != 0 )
        {
          sub_1412D33C0(a1: v31);
        }
        goto LABEL_38;
      }
    }
    goto LABEL_37;
  }
LABEL_41:
  a1 = v35;
  *v35 = *(_DWORD *)(*v4 + 16LL);
  return a1;
}
