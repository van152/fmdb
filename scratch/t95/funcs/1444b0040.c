__int64 *__fastcall sub_1444B0040(__int64 *a1, __int64 a2)
{
  __int64 **v4; // rax
  __int64 *v5; // rsi
  __int64 *v6; // r13
  _QWORD *v7; // rbx
  __int64 v8; // r14
  __int64 v9; // rax
  __int64 v10; // r15
  unsigned __int64 v11; // rcx
  unsigned __int64 v12; // rax
  __int64 v13; // r8
  unsigned __int64 v14; // rdx
  unsigned __int64 v15; // rax
  __int64 v16; // rdi
  _QWORD *v17; // r14
  __int64 v18; // r14
  __int64 v19; // rdi
  unsigned __int64 v20; // rcx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rcx
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
  v4 = *(__int64 ***)(qword_141B60160 + 128);
  v5 = *v4;
  v6 = v4[1];
  if ( *v4 == v6 )
  {
    v23 = 0;
    v7 = nullptr;
    goto LABEL_34;
  }
  v7 = nullptr;
  v26 = a2;
  do
  {
    v8 = *v5;
    if ( *v5 != 0 )
    {
      v9 = *(_QWORD *)(v8 + 32);
      if ( v9 != 0 && *(_DWORD *)(v9 + 12) == *(_DWORD *)(a2 + 12) )
      {
        if ( v7 != (_QWORD *)a1[2] )
        {
          *v7 = v8;
          v7 = (_QWORD *)(a1[1] + 8);
          a1[1] = (__int64)v7;
          goto LABEL_7;
        }
        v10 = (__int64)v7 - *a1;
        v11 = v10 >> 3;
        v12 = (unsigned __int64)(v10 >> 3) >> 1;
        v13 = 0x1FFFFFFFFFFFFFFFLL;
        v14 = 0x1FFFFFFFFFFFFFFFLL - v12;
        v15 = (v10 >> 3) + v12;
        if ( v15 <= (v10 >> 3) + 1 )
          v15 = v11 + 1;
        if ( v11 <= v14 )
          v13 = v15;
        v25 = v13;
        v16 = sub_1407E4490(qword_141ABD470, 8 * v13);
        *(_QWORD *)(v16 + v10) = v8;
        v17 = (_QWORD *)a1[1];
        sub_141758A00();
        if ( v17 != v7 )
          sub_141758A00();
        v18 = v16;
        v19 = *a1;
        if ( *a1 == 0 )
          goto LABEL_29;
        v20 = a1[2] - v19;
        if ( v20 == -1 )
        {
          v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_28;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_28;
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
            goto LABEL_29;
          }
        }
LABEL_28:
        MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_29:
        *a1 = v18;
        v7 = (_QWORD *)(v18 + 8 * ((v10 >> 3) + 1));
        a1[1] = (__int64)v7;
        a1[2] = v18 + 8 * v25;
        a2 = v26;
      }
    }
LABEL_7:
    ++v5;
  }
  while ( v5 != v6 );
  v23 = *a1;
LABEL_34:
  sub_140054D70(v23, v7, ((__int64)v7 - v23) >> 3, sub_14119FD70);
  return a1;
}
