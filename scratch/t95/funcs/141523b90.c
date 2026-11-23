// THUNK ALIAS -> sub_1444B3310 (jmp:0x141523b90->0x1444b3310)
__int64 *__fastcall sub_1444B3310(__int64 *a1, __int64 a2, int a3)
{
  __int64 v6; // rax
  unsigned __int64 v7; // rax
  __int64 v8; // rcx
  _QWORD *v9; // rbx
  __int64 v10; // r14
  __int64 v11; // r15
  __int64 v12; // r12
  unsigned __int64 v13; // rcx
  unsigned __int64 v14; // rax
  __int64 v15; // r8
  unsigned __int64 v16; // rdx
  unsigned __int64 v17; // rax
  __int64 v18; // rsi
  _QWORD *v19; // rdi
  __int64 v20; // rdi
  unsigned __int64 v21; // rcx
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int64 v25; // [rsp+30h] [rbp-20h]
  __int64 v26; // [rsp+38h] [rbp-18h]
  __int64 v27; // [rsp+40h] [rbp-10h]
  int v28; // [rsp+4Ch] [rbp-4h]

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
  *((_DWORD *)a1 + 6) = a3;
  v6 = *(_QWORD *)(a2 + 32) - *(_QWORD *)(a2 + 24);
  if ( v6 != 0 )
  {
    v7 = v6 >> 3;
    v8 = 1;
    if ( v7 >= 2 )
      v8 = v7;
    v9 = nullptr;
    v10 = 0;
    v28 = a3;
    v26 = a2;
    v27 = v8;
    do
    {
      v11 = *(_QWORD *)(*(_QWORD *)(a2 + 24) + 8 * v10);
      if ( *(_DWORD *)(v11 + 8) == a3 )
      {
        if ( v9 == (_QWORD *)a1[2] )
        {
          v12 = (__int64)v9 - *a1;
          v13 = v12 >> 3;
          v14 = (unsigned __int64)(v12 >> 3) >> 1;
          v15 = 0x1FFFFFFFFFFFFFFFLL;
          v16 = 0x1FFFFFFFFFFFFFFFLL - v14;
          v17 = (v12 >> 3) + v14;
          if ( v17 <= (v12 >> 3) + 1 )
            v17 = v13 + 1;
          if ( v13 <= v16 )
            v15 = v17;
          v25 = v15;
          v18 = sub_1407E4490(qword_141ABD470, 8 * v15);
          *(_QWORD *)(v18 + v12) = v11;
          v19 = (_QWORD *)a1[1];
          sub_141758A00();
          if ( v19 != v9 )
            sub_141758A00();
          v20 = *a1;
          if ( *a1 != 0 )
          {
            v21 = a1[2] - v20;
            if ( v21 == -1 )
            {
              v21 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_28;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_28;
            }
            v22 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v22) >> 3 > v21 && (v23 = *(_QWORD *)(v22 + 8 * v21)) != 0 )
            {
              MEMORY[0x1419475D8](v23 + 32, v20 - *(unsigned int *)(v23 + 120));
              if ( (*(_BYTE *)(v23 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) == 0)
                && *(_BYTE *)(v23 + 97) != 0 )
              {
                sub_1412D33C0(v23);
              }
            }
            else
            {
LABEL_28:
              MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *a1 = v18;
          v9 = (_QWORD *)(v18 + 8 * ((v12 >> 3) + 1));
          a1[1] = (__int64)v9;
          a1[2] = v18 + 8 * v25;
          a3 = v28;
          a2 = v26;
          v8 = v27;
          goto LABEL_9;
        }
        *v9 = v11;
        v9 = (_QWORD *)(a1[1] + 8);
        a1[1] = (__int64)v9;
      }
LABEL_9:
      ++v10;
    }
    while ( v8 != v10 );
  }
  return a1;
}
