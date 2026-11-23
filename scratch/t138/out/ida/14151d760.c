_DWORD *__fastcall sub_14151D760(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  __int64 v6; // rsi
  __int64 v7; // r15
  __int64 v8; // r13
  __int64 v9; // r12
  __int64 v10; // rbp
  unsigned __int64 v11; // rcx
  __int64 v12; // r8
  __int64 v13; // r14
  bool v14; // al
  __int64 v15; // r12
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 *v23; // r15
  __int64 v24; // r14
  unsigned __int64 v25; // rax
  unsigned __int64 v26; // r13
  unsigned __int64 v27; // rcx
  unsigned __int64 v28; // r13
  __int64 v29; // rbp
  __int64 *v30; // rsi
  __int64 v31; // rsi
  unsigned __int64 v32; // rcx
  __int64 v33; // r8
  __int64 v34; // r14
  bool v35; // al
  unsigned __int8 v37; // [rsp+24h] [rbp-64h] BYREF
  char v38; // [rsp+25h] [rbp-63h] BYREF
  char v39; // [rsp+26h] [rbp-62h] BYREF
  char v40; // [rsp+27h] [rbp-61h] BYREF
  __int64 v41; // [rsp+28h] [rbp-60h] BYREF
  unsigned int v42; // [rsp+34h] [rbp-54h] BYREF
  _DWORD *v43; // [rsp+38h] [rbp-50h]
  unsigned __int64 v44; // [rsp+40h] [rbp-48h]

  v42 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v42, a3: 4);
  v6 = v42;
  if ( qword_141AA7808 <= (unsigned __int64)v42 )
  {
LABEL_51:
    *a1 = 1;
    return a1;
  }
  v43 = a1;
  v7 = *a3;
  if ( (a3[2] - *a3) >> 3 < (unsigned __int64)v42 )
  {
    v8 = a3[1];
    v9 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v42);
    sub_141758A00(a1: v9, a2: *a3, a3: a3[1] - *a3);
    v10 = *a3;
    if ( *a3 == 0 )
    {
LABEL_13:
      *a3 = v9;
      a3[1] = v9 + v8 - v7;
      a3[2] = v9 + 8 * v6;
      LODWORD(v6) = v42;
      goto LABEL_14;
    }
    v11 = a3[2] - v10;
    if ( v11 == -1 )
    {
      v11 = *(unsigned int *)(v10 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v10 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v12 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v12) >> 3 > v11 )
    {
      v13 = *(_QWORD *)(v12 + 8 * v11);
      if ( v13 != 0 )
      {
        MEMORY[0x1419475D8](a1: v13 + 32, a2: v10 - *(unsigned int *)(v13 + 120));
        v14 = *(_BYTE *)(v13 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 64)) != 0;
        if ( !v14 && *(_BYTE *)(v13 + 97) != 0 )
          sub_1412D33C0(a1: v13);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( (_DWORD)v6 != 0 )
  {
    v15 = 0;
    while ( 1 )
    {
      v41 = 16711680;
      v16 = *a2;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v37, a3: 1);
      if ( *(_DWORD *)(v16 + 16) != 0
        || (v17 = *a2,
            (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v41, a3: 2),
            *(_DWORD *)(v17 + 16) != 0)
        || (v18 = *a2,
            (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: (char *)&v41 + 2,
              a3: 1),
            *(_DWORD *)(v18 + 16) != 0)
        || (v19 = *a2,
            (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: (char *)&v41 + 3,
              a3: 1),
            *(_DWORD *)(v19 + 16) != 0) )
      {
LABEL_50:
        a1 = v43;
        goto LABEL_51;
      }
      if ( v37 >= 2u )
      {
        v20 = *a2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v40, a3: 1);
        if ( *(_DWORD *)(v20 + 16) != 0 )
          goto LABEL_50;
        v21 = *a2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v39, a3: 1);
        if ( *(_DWORD *)(v21 + 16) != 0 )
          goto LABEL_50;
        v22 = *a2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v38, a3: 1);
        if ( *(_DWORD *)(v22 + 16) != 0 )
          goto LABEL_50;
        BYTE4(v41) = v40;
        BYTE5(v41) = v39;
        BYTE6(v41) = v38;
      }
      if ( *(_DWORD *)(*a2 + 16LL) != 0 )
        goto LABEL_50;
      v23 = (__int64 *)a3[1];
      if ( v23 == (__int64 *)a3[2] )
        break;
      *v23 = v41;
      a3[1] += 8;
LABEL_17:
      if ( ++v15 >= (unsigned __int64)v42 )
        goto LABEL_52;
    }
    v24 = (__int64)v23 - *a3;
    v25 = v24 >> 3;
    v26 = (unsigned __int64)(v24 >> 3) >> 1;
    v27 = 0x1FFFFFFFFFFFFFFFLL - v26;
    v28 = (v24 >> 3) + v26;
    v44 = (v24 >> 3) + 1;
    if ( v28 <= v44 )
      v28 = v25 + 1;
    if ( v25 > v27 )
      v28 = 0x1FFFFFFFFFFFFFFFLL;
    v29 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v28);
    *(_QWORD *)(v29 + v24) = v41;
    v30 = (__int64 *)a3[1];
    sub_141758A00(a1: v29, a2: *a3, a3: (char *)v23 - *a3);
    if ( v30 != v23 )
      sub_141758A00(a1: v29 + v24 + 8, a2: v23, a3: a3[1] - (_QWORD)v23);
    v31 = *a3;
    if ( *a3 == 0 )
    {
LABEL_45:
      *a3 = v29;
      a3[1] = v29 + 8 * v44;
      a3[2] = v29 + 8 * v28;
      goto LABEL_17;
    }
    v32 = a3[2] - v31;
    if ( v32 == -1 )
    {
      v32 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_44:
        MEMORY[0x141948990](a1: v31 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_45;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_44;
    }
    v33 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v32 )
    {
      v34 = *(_QWORD *)(v33 + 8 * v32);
      if ( v34 != 0 )
      {
        MEMORY[0x1419475D8](a1: v34 + 32, a2: v31 - *(unsigned int *)(v34 + 120));
        v35 = *(_BYTE *)(v34 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
        if ( !v35 && *(_BYTE *)(v34 + 97) != 0 )
          sub_1412D33C0(a1: v34);
        goto LABEL_45;
      }
    }
    goto LABEL_44;
  }
LABEL_52:
  a1 = v43;
  *v43 = *(_DWORD *)(*a2 + 16LL);
  return a1;
}
