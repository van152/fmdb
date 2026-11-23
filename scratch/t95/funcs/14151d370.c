// THUNK ALIAS -> sub_1444A3630 (jmp:0x14151d370->0x1444a3630)
__int64 *__fastcall sub_1444A3630(__int64 *a1, __int64 a2)
{
  __int64 **v4; // rax
  __int64 *v5; // rsi
  __int64 *v6; // r13
  _QWORD *v7; // rdi
  __int64 v8; // r14
  __int64 v9; // r15
  unsigned __int64 v10; // rcx
  unsigned __int64 v11; // rax
  __int64 v12; // r8
  unsigned __int64 v13; // rdx
  unsigned __int64 v14; // rax
  __int64 v15; // rbx
  _QWORD *v16; // r14
  __int64 v17; // rdi
  unsigned __int64 v18; // rcx
  __int64 v19; // r8
  __int64 v20; // r14
  __int64 v22; // [rsp+30h] [rbp-10h]
  __int64 v23; // [rsp+38h] [rbp-8h]

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
  v4 = *(__int64 ***)(qword_141B600F0 + 128);
  v5 = *v4;
  v6 = v4[1];
  if ( *v4 != v6 )
  {
    v7 = nullptr;
    v23 = a2;
    while ( 1 )
    {
      v8 = *v5;
      if ( *v5 != 0 && *(_QWORD *)(v8 + 24) == a2 )
      {
        if ( v7 == (_QWORD *)a1[2] )
          break;
        *v7 = v8;
        v7 = (_QWORD *)(a1[1] + 8);
        a1[1] = (__int64)v7;
      }
LABEL_7:
      if ( ++v5 == v6 )
        return a1;
    }
    v9 = (__int64)v7 - *a1;
    v10 = v9 >> 3;
    v11 = (unsigned __int64)(v9 >> 3) >> 1;
    v12 = 0x1FFFFFFFFFFFFFFFLL;
    v13 = 0x1FFFFFFFFFFFFFFFLL - v11;
    v14 = (v9 >> 3) + v11;
    if ( v14 <= (v9 >> 3) + 1 )
      v14 = v10 + 1;
    if ( v10 <= v13 )
      v12 = v14;
    v22 = v12;
    v15 = sub_1407E4490(qword_141ABD470, 8 * v12);
    *(_QWORD *)(v15 + v9) = v8;
    v16 = (_QWORD *)a1[1];
    sub_141758A00();
    if ( v16 != v7 )
      sub_141758A00();
    v17 = *a1;
    if ( *a1 == 0 )
    {
LABEL_28:
      *a1 = v15;
      v7 = (_QWORD *)(v15 + 8 * ((v9 >> 3) + 1));
      a1[1] = (__int64)v7;
      a1[2] = v15 + 8 * v22;
      a2 = v23;
      goto LABEL_7;
    }
    v18 = a1[2] - v17;
    if ( v18 == -1 )
    {
      v18 = *(unsigned int *)(v17 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_27:
        MEMORY[0x141948990](v17 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_28;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_27;
    }
    v19 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v19) >> 3 > v18 )
    {
      v20 = *(_QWORD *)(v19 + 8 * v18);
      if ( v20 != 0 )
      {
        MEMORY[0x1419475D8](v20 + 32, v17 - *(unsigned int *)(v20 + 120));
        if ( (*(_BYTE *)(v20 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v20 + 64)) == 0)
          && *(_BYTE *)(v20 + 97) != 0 )
        {
          sub_1412D33C0(v20);
        }
        goto LABEL_28;
      }
    }
    goto LABEL_27;
  }
  return a1;
}
