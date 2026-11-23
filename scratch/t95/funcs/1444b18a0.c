__int64 *__fastcall sub_1444B18A0(__int64 *a1, __int64 a2, char a3)
{
  __int64 v6; // r14
  __int64 v7; // r14
  __int64 v8; // r15
  __int64 v9; // rsi
  _QWORD *v10; // rdi
  __int64 v11; // r14
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // r12
  unsigned __int64 v14; // rcx
  unsigned __int64 v15; // r12
  __int64 v16; // rbx
  _QWORD *v17; // rsi
  __int64 v18; // rdi
  unsigned __int64 v19; // rcx
  __int64 v20; // rbx
  __int64 v21; // rsi
  bool v22; // al
  unsigned __int64 v24; // [rsp+28h] [rbp-28h]
  __int64 v25; // [rsp+30h] [rbp-20h]
  __int64 v26; // [rsp+38h] [rbp-18h]
  __int64 v27; // [rsp+40h] [rbp-10h]
  char v28; // [rsp+4Fh] [rbp-1h]

  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  *((_BYTE *)a1 + 24) = a3;
  v6 = *(_QWORD *)(*(_QWORD *)(a2 + 176) + 8LL) - **(_QWORD **)(a2 + 176);
  if ( v6 != 0 )
  {
    v7 = v6 >> 3;
    v8 = 0;
    v28 = a3;
    v25 = a2;
    v26 = v7;
    while ( 1 )
    {
      v9 = *(_QWORD *)(**(_QWORD **)(a2 + 176) + 8 * v8);
      if ( v9 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 56LL))(v9) == a3 )
      {
        v10 = (_QWORD *)a1[1];
        if ( v10 == (_QWORD *)a1[2] )
          break;
        *v10 = v9;
        a1[1] += 8;
      }
LABEL_7:
      if ( v7 == ++v8 )
        return a1;
    }
    v11 = (__int64)v10 - *a1;
    v12 = v11 >> 3;
    v13 = (unsigned __int64)(v11 >> 3) >> 1;
    v14 = 0x1FFFFFFFFFFFFFFFLL - v13;
    v15 = (v11 >> 3) + v13;
    v24 = (v11 >> 3) + 1;
    if ( v15 <= v24 )
      v15 = v12 + 1;
    if ( v12 > v14 )
      v15 = 0x1FFFFFFFFFFFFFFFLL;
    v16 = sub_1407E4490(qword_141ABD470, 8 * v15);
    *(_QWORD *)(v16 + v11) = v9;
    v17 = (_QWORD *)a1[1];
    sub_141758A00();
    if ( v17 != v10 )
      sub_141758A00();
    v18 = *a1;
    v7 = v26;
    if ( *a1 == 0 )
    {
LABEL_27:
      *a1 = v16;
      a1[1] = v16 + 8 * v24;
      a1[2] = v16 + 8 * v15;
      a3 = v28;
      a2 = v25;
      goto LABEL_7;
    }
    v27 = v16;
    v19 = a1[2] - v18;
    if ( v19 == -1 )
    {
      v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_26:
        MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
        v16 = v27;
        goto LABEL_27;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_26;
    }
    v20 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19 )
    {
      v21 = *(_QWORD *)(v20 + 8 * v19);
      if ( v21 != 0 )
      {
        MEMORY[0x1419475D8](v21 + 32, v18 - *(unsigned int *)(v21 + 120));
        v22 = *(_BYTE *)(v21 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) != 0;
        v16 = v27;
        if ( !v22 && *(_BYTE *)(v21 + 97) != 0 )
          sub_1412D33C0(v21);
        goto LABEL_27;
      }
    }
    goto LABEL_26;
  }
  return a1;
}
