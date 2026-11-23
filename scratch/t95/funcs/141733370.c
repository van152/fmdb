// THUNK ALIAS -> sub_14475DBB0 (jmp:0x141733370->0x14475dbb0)
__int64 *__fastcall sub_14475DBB0(__int64 *a1, __int64 a2)
{
  unsigned __int64 v4; // rax
  __int64 v5; // rbx
  __int64 *v6; // rdi
  __int64 v7; // r14
  __int64 v8; // rax
  __int64 v9; // rsi
  __int64 v10; // rbx
  unsigned __int64 v11; // rcx
  unsigned __int64 v12; // r13
  unsigned __int64 v13; // rax
  __int64 v14; // r8
  unsigned __int64 v15; // rdx
  unsigned __int64 v16; // rax
  __int64 v17; // r15
  __int64 *v18; // rsi
  __int64 v19; // rdi
  unsigned __int64 v20; // rcx
  __int64 v21; // rbx
  __int64 v22; // rsi
  __int64 v24; // [rsp+28h] [rbp-18h]
  __int64 v25; // [rsp+30h] [rbp-10h]
  __int64 v26; // [rsp+38h] [rbp-8h]

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
  v4 = *(_QWORD *)(a2 + 56) - *(_QWORD *)(a2 + 48);
  if ( v4 != 0 )
  {
    v5 = 1;
    if ( v4 >= 2 )
      v5 = *(_QWORD *)(a2 + 56) - *(_QWORD *)(a2 + 48);
    v6 = nullptr;
    v7 = 0;
    v25 = a2;
    v26 = v5;
    while ( 1 )
    {
      v8 = sub_141750CC0(16);
      v9 = v8;
      *(_QWORD *)v8 = a2;
      *(_DWORD *)(v8 + 8) = v7;
      if ( v6 == (__int64 *)a1[2] )
        break;
      *v6 = v8;
      v6 = (__int64 *)(a1[1] + 8);
      a1[1] = (__int64)v6;
LABEL_9:
      if ( v5 == ++v7 )
        return a1;
    }
    v10 = (__int64)v6 - *a1;
    v11 = v10 >> 3;
    v12 = (v10 >> 3) + 1;
    v13 = (unsigned __int64)(v10 >> 3) >> 1;
    v14 = 0x1FFFFFFFFFFFFFFFLL;
    v15 = 0x1FFFFFFFFFFFFFFFLL - v13;
    v16 = (v10 >> 3) + v13;
    if ( v16 <= v12 )
      v16 = v11 + 1;
    if ( v11 <= v15 )
      v14 = v16;
    v24 = v14;
    v17 = sub_1407E4490(qword_141ABD470, 8 * v14);
    *(_QWORD *)(v17 + v10) = v9;
    v18 = (__int64 *)a1[1];
    sub_141758A00();
    if ( v18 != v6 )
      sub_141758A00();
    v19 = *a1;
    if ( *a1 == 0 )
    {
LABEL_28:
      *a1 = v17;
      v6 = (__int64 *)(v17 + 8 * v12);
      a1[1] = (__int64)v6;
      a1[2] = v17 + 8 * v24;
      a2 = v25;
      v5 = v26;
      goto LABEL_9;
    }
    v20 = a1[2] - v19;
    if ( v20 == -1 )
    {
      v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_27:
        MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_28;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_27;
    }
    v21 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20 )
    {
      v22 = *(_QWORD *)(v21 + 8 * v20);
      if ( v22 != 0 )
      {
        MEMORY[0x1419475D8](v22 + 32, v19 - *(unsigned int *)(v22 + 120));
        if ( (*(_BYTE *)(v22 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) == 0)
          && *(_BYTE *)(v22 + 97) != 0 )
        {
          sub_1412D33C0(v22);
        }
        goto LABEL_28;
      }
    }
    goto LABEL_27;
  }
  return a1;
}
