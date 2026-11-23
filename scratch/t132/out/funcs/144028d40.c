__int64 __fastcall sub_144028D40(__int64 a1, unsigned int a2, unsigned int a3, unsigned int a4)
{
  __int64 v8; // rbp
  __int64 v9; // rbp
  __int64 v10; // rsi
  __int64 v11; // rax
  __int64 *v12; // rdi
  __int64 *v13; // rbx
  __int64 v14; // rbp
  unsigned __int64 v15; // rax
  unsigned __int64 v16; // r12
  unsigned __int64 v17; // r15
  unsigned __int64 v18; // rdx
  unsigned __int64 v19; // r15
  __int64 v20; // r14
  __int64 *v21; // r13
  __int64 v22; // rbx
  unsigned __int64 v23; // rcx
  __int64 v24; // rbp
  __int64 v25; // rbp
  bool v26; // al

  v8 = *(_QWORD *)(*(_QWORD *)(a1 + 176) + 8LL) - **(_QWORD **)(a1 + 176);
  if ( v8 == 0 )
  {
LABEL_8:
    v11 = sub_1414D00D0(a1: a2);
    if ( v11 == 0 )
      return 0;
    v10 = v11;
    (*(void (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v11 + 144LL))(a1: v11, a2: a3);
    (*(void (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v10 + 152LL))(a1: v10, a2: a4);
    v12 = *(__int64 **)(a1 + 176);
    v13 = (__int64 *)v12[1];
    if ( v13 != (__int64 *)v12[2] )
    {
      *v13 = v10;
      v12[1] += 8;
      return v10;
    }
    v14 = (__int64)v13 - *v12;
    v15 = v14 >> 3;
    v16 = (v14 >> 3) + 1;
    v17 = (unsigned __int64)(v14 >> 3) >> 1;
    v18 = 0x1FFFFFFFFFFFFFFFLL - v17;
    v19 = (v14 >> 3) + v17;
    if ( v19 <= v16 )
      v19 = v15 + 1;
    if ( v15 > v18 )
      v19 = 0x1FFFFFFFFFFFFFFFLL;
    v20 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v19);
    *(_QWORD *)(v20 + v14) = v10;
    v21 = (__int64 *)v12[1];
    sub_141758A00(a1: v20, a2: *v12, a3: (char *)v13 - *v12);
    if ( v21 != v13 )
      sub_141758A00(a1: v20 + v14 + 8, a2: v13, a3: v12[1] - (_QWORD)v13);
    v22 = *v12;
    if ( *v12 == 0 )
    {
LABEL_28:
      *v12 = v20;
      v12[1] = v20 + 8 * v16;
      v12[2] = v20 + 8 * v19;
      return v10;
    }
    v23 = v12[2] - v22;
    if ( v23 == -1 )
    {
      v23 = *(unsigned int *)(v22 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_27:
        MEMORY[0x141948990](a1: v22 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_28;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_27;
    }
    v24 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 > v23 )
    {
      v25 = *(_QWORD *)(v24 + 8 * v23);
      if ( v25 != 0 )
      {
        MEMORY[0x1419475D8](a1: v25 + 32, a2: v22 - *(unsigned int *)(v25 + 120));
        v26 = *(_BYTE *)(v25 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) != 0;
        if ( !v26 && *(_BYTE *)(v25 + 97) != 0 )
          sub_1412D33C0(a1: v25);
        goto LABEL_28;
      }
    }
    goto LABEL_27;
  }
  v9 = v8 >> 3;
  while ( 1 )
  {
    v10 = *(_QWORD *)(**(_QWORD **)(a1 + 176) + 8 * v9 - 8);
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v10 + 56LL))(a1: v10) == (_BYTE)a2
      && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v10 + 64LL))(a1: v10) == a3
      && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v10 + 72LL))(a1: v10) == a4 )
    {
      return v10;
    }
    if ( --v9 == 0 )
      goto LABEL_8;
  }
}
