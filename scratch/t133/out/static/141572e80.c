_DWORD *__fastcall sub_141572E80(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // rbx
  __int64 v6; // rbp
  __int64 v7; // r15
  unsigned __int64 v8; // rax
  __int64 *v9; // rdi
  __int64 v10; // r13
  __int64 v11; // r12
  __int64 v12; // rsi
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  __int64 v17; // r12
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  _QWORD *v21; // rbp
  __int64 v22; // r14
  unsigned __int64 v23; // rax
  unsigned __int64 v24; // r15
  unsigned __int64 v25; // rcx
  unsigned __int64 v26; // r15
  unsigned __int64 v27; // rbx
  __int64 v28; // rsi
  __int64 v29; // rdx
  _QWORD *v30; // r13
  bool v31; // zf
  __int64 v32; // rbp
  unsigned __int64 v33; // rcx
  __int64 v34; // r8
  __int64 v35; // r14
  char v37; // [rsp+23h] [rbp-65h] BYREF
  unsigned int v38; // [rsp+24h] [rbp-64h] BYREF
  __int64 v39; // [rsp+28h] [rbp-60h] BYREF
  __int64 *v40; // [rsp+30h] [rbp-58h]
  _DWORD *v41; // [rsp+38h] [rbp-50h]
  _QWORD *v42; // [rsp+40h] [rbp-48h]

  v4 = a2;
  v38 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v38, a3: 4);
  v6 = v38;
  if ( qword_141AA7808 <= (unsigned __int64)v38 )
  {
LABEL_45:
    *a1 = 1;
    return a1;
  }
  v41 = a1;
  v7 = *a3;
  v8 = (a3[2] - *a3) >> 3;
  v40 = a3;
  if ( v8 < v38 )
  {
    v9 = a3;
    v10 = a3[1];
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v38);
    sub_141758A00(a1: v11, a2: *v9, a3: v9[1] - *v9);
    v12 = *v9;
    if ( *v9 == 0 )
    {
LABEL_13:
      *v9 = v11;
      v9[1] = v11 + v10 - v7;
      v9[2] = v11 + 8 * v6;
      LODWORD(v6) = v38;
      a3 = v9;
      goto LABEL_14;
    }
    v13 = v9[2] - v12;
    if ( v13 == -1 )
    {
      v13 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v12 - *(unsigned int *)(qword_141ABD470 + 48));
        v9 = v40;
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 != 0 )
      {
        MEMORY[0x1419475D8](a1: v15 + 32, a2: v12 - *(unsigned int *)(v15 + 120));
        v16 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        v9 = v40;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(a1: v15);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( (_DWORD)v6 != 0 )
  {
    v17 = 0;
    v42 = v4;
    while ( 1 )
    {
      LODWORD(v39) = 0;
      WORD2(v39) = 0;
      v18 = *v4;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v37, a3: 1);
      if ( *(_DWORD *)(v18 + 16) != 0
        || (v19 = *v4,
            (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v39, a3: 4),
            *(_DWORD *)(v19 + 16) != 0)
        || (v20 = *v4,
            (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v4 + 40LL))(
              a1: *v4,
              a2: (char *)&v39 + 4,
              a3: 2),
            *(_DWORD *)(v20 + 16) != 0) )
      {
        a1 = v41;
        goto LABEL_45;
      }
      if ( *(_DWORD *)(*v4 + 16LL) != 0 )
        goto LABEL_43;
      v21 = (_QWORD *)a3[1];
      if ( v21 == (_QWORD *)a3[2] )
        break;
      *v21 = v39;
      a3[1] += 8;
LABEL_17:
      if ( ++v17 >= (unsigned __int64)v38 )
        goto LABEL_43;
    }
    v22 = (__int64)v21 - *a3;
    v23 = v22 >> 3;
    v24 = (unsigned __int64)(v22 >> 3) >> 1;
    v25 = 0x1FFFFFFFFFFFFFFFLL - v24;
    v26 = (v22 >> 3) + v24;
    v27 = (v22 >> 3) + 1;
    if ( v26 <= v27 )
      v26 = v23 + 1;
    if ( v23 > v25 )
      v26 = 0x1FFFFFFFFFFFFFFFLL;
    v28 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v26);
    *(_QWORD *)(v28 + v22) = v39;
    v29 = *a3;
    v30 = (_QWORD *)v40[1];
    sub_141758A00(a1: v28, a2: v29, a3: (char *)v21 - v29);
    v31 = v30 == v21;
    a3 = v40;
    if ( !v31 )
      sub_141758A00(a1: v28 + v22 + 8, a2: v21, a3: v40[1] - (_QWORD)v21);
    v32 = *a3;
    if ( *a3 == 0 )
    {
LABEL_40:
      *a3 = v28;
      a3[1] = v28 + 8 * v27;
      a3[2] = v28 + 8 * v26;
      v4 = v42;
      goto LABEL_17;
    }
    v33 = a3[2] - v32;
    if ( v33 == -1 )
    {
      v33 = *(unsigned int *)(v32 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_39:
        MEMORY[0x141948990](a1: v32 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_40;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_39;
    }
    v34 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v34) >> 3 > v33 )
    {
      v35 = *(_QWORD *)(v34 + 8 * v33);
      if ( v35 != 0 )
      {
        MEMORY[0x1419475D8](a1: v35 + 32, a2: v32 - *(unsigned int *)(v35 + 120));
        if ( (*(_BYTE *)(v35 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v35 + 64)) == 0)
          && *(_BYTE *)(v35 + 97) != 0 )
        {
          sub_1412D33C0(a1: v35);
        }
        goto LABEL_40;
      }
    }
    goto LABEL_39;
  }
LABEL_43:
  a1 = v41;
  *v41 = *(_DWORD *)(*v4 + 16LL);
  return a1;
}
