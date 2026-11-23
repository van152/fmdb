__int64 *__fastcall sub_1444C6A80(__int64 *a1, __int64 a2)
{
  __int64 v4; // rax
  unsigned __int64 v5; // rax
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // r13
  __int64 *v9; // rdi
  int v10; // eax
  __int64 v11; // rax
  __int64 v12; // rsi
  __int64 v13; // r14
  unsigned __int64 v14; // rcx
  unsigned __int64 v15; // rax
  unsigned __int64 v16; // rdx
  unsigned __int64 v17; // rax
  __int64 v18; // rbx
  __int64 v19; // r15
  __int64 *v20; // rsi
  __int64 v21; // rdi
  unsigned __int64 v22; // rcx
  __int64 v23; // rbx
  __int64 v24; // rsi
  bool v25; // al
  unsigned __int64 v27; // [rsp+20h] [rbp-20h]
  __int64 v28; // [rsp+28h] [rbp-18h]
  __int64 v29; // [rsp+30h] [rbp-10h]
  __int64 v30; // [rsp+38h] [rbp-8h]

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
  v4 = *(_QWORD *)(a2 + 32) - *(_QWORD *)(a2 + 24);
  if ( (unsigned __int64)v4 >= 9 )
  {
    v5 = v4 >> 3;
    v6 = 2;
    if ( v5 >= 3 )
      v6 = v5;
    v7 = v6 - 1;
    v8 = 0;
    v9 = nullptr;
    v28 = v7;
    v29 = a2;
    while ( 1 )
    {
      v10 = *(unsigned __int8 *)(*(_QWORD *)(*(_QWORD *)(a2 + 24) + 8 * v8 + 8) + 40LL);
      if ( v10 != 22 && v10 != 44 )
      {
        v11 = sub_141750CC0(16);
        v12 = v11;
        *(_QWORD *)v11 = a2;
        *(_DWORD *)(v11 + 8) = v8;
        if ( v9 == (__int64 *)a1[2] )
          break;
        *v9 = v11;
        v9 = (__int64 *)(a1[1] + 8);
        a1[1] = (__int64)v9;
      }
LABEL_9:
      if ( v7 == ++v8 )
        return a1;
    }
    v13 = (__int64)v9 - *a1;
    v14 = v13 >> 3;
    v15 = (unsigned __int64)(v13 >> 3) >> 1;
    v16 = 0x1FFFFFFFFFFFFFFFLL - v15;
    v17 = (v13 >> 3) + v15;
    v27 = (v13 >> 3) + 1;
    if ( v17 <= v27 )
      v17 = v14 + 1;
    v18 = 0x1FFFFFFFFFFFFFFFLL;
    if ( v14 <= v16 )
      v18 = v17;
    v19 = sub_1407E4490(qword_141ABD470, 8 * v18);
    *(_QWORD *)(v19 + v13) = v12;
    v20 = (__int64 *)a1[1];
    sub_141758A00();
    if ( v20 != v9 )
      sub_141758A00();
    v21 = *a1;
    a2 = v29;
    if ( *a1 == 0 )
    {
LABEL_29:
      *a1 = v19;
      v9 = (__int64 *)(v19 + 8 * v27);
      a1[1] = (__int64)v9;
      a1[2] = v19 + 8 * v18;
      v7 = v28;
      goto LABEL_9;
    }
    v30 = v18;
    v22 = a1[2] - v21;
    if ( v22 == -1 )
    {
      v22 = *(unsigned int *)(v21 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_28:
        MEMORY[0x141948990](v21 - *(unsigned int *)(qword_141ABD470 + 48));
        v18 = v30;
        goto LABEL_29;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_28;
    }
    v23 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v23) >> 3 > v22 )
    {
      v24 = *(_QWORD *)(v23 + 8 * v22);
      if ( v24 != 0 )
      {
        MEMORY[0x1419475D8](v24 + 32, v21 - *(unsigned int *)(v24 + 120));
        v25 = *(_BYTE *)(v24 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) != 0;
        v18 = v30;
        if ( !v25 && *(_BYTE *)(v24 + 97) != 0 )
          sub_1412D33C0(v24);
        goto LABEL_29;
      }
    }
    goto LABEL_28;
  }
  return a1;
}
