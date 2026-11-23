// THUNK ALIAS -> sub_144765380 (jmp:0x141735860->0x144765380)
__int64 *__fastcall sub_144765380(__int64 *a1, __int64 a2)
{
  __int64 **v4; // rax
  __int64 *v5; // rbx
  __int64 *v6; // r15
  __int64 v7; // rsi
  __int64 *v8; // rdi
  __int64 v9; // r13
  unsigned __int64 v10; // rax
  unsigned __int64 v11; // r14
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // r14
  __int64 v14; // r15
  __int64 *v15; // rsi
  __int64 v16; // rsi
  unsigned __int64 v17; // rcx
  __int64 v18; // rdi
  __int64 v19; // rdi
  __int64 v21; // [rsp+30h] [rbp-10h]
  __int64 *v22; // [rsp+38h] [rbp-8h]

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
  v4 = *(__int64 ***)(qword_141B5FDD0 + 128);
  v5 = *v4;
  v6 = v4[1];
  if ( *v4 != v6 )
  {
    v21 = a2;
    v22 = v4[1];
    do
    {
      v7 = *v5;
      if ( sub_141048140(*v5, *(_DWORD *)(a2 + 12), -1, -1) != nullptr )
      {
        v8 = (__int64 *)a1[1];
        if ( v8 == (__int64 *)a1[2] )
        {
          v9 = (__int64)v8 - *a1;
          v10 = v9 >> 3;
          v11 = (unsigned __int64)(v9 >> 3) >> 1;
          v12 = 0x1FFFFFFFFFFFFFFFLL - v11;
          v13 = (v9 >> 3) + v11;
          if ( v13 <= (v9 >> 3) + 1 )
            v13 = v10 + 1;
          if ( v10 > v12 )
            v13 = 0x1FFFFFFFFFFFFFFFLL;
          v14 = sub_1407E4490(qword_141ABD470, 8 * v13);
          *(_QWORD *)(v14 + v9) = v7;
          v15 = (__int64 *)a1[1];
          sub_141758A00();
          if ( v15 != v8 )
            sub_141758A00();
          v16 = *a1;
          if ( *a1 != 0 )
          {
            v17 = a1[2] - v16;
            if ( v17 == -1 )
            {
              v17 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_26;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_26;
            }
            v18 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v18) >> 3 > v17 && (v19 = *(_QWORD *)(v18 + 8 * v17)) != 0 )
            {
              MEMORY[0x1419475D8](v19 + 32, v16 - *(unsigned int *)(v19 + 120));
              if ( (*(_BYTE *)(v19 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v19 + 64)) == 0)
                && *(_BYTE *)(v19 + 97) != 0 )
              {
                sub_1412D33C0(v19);
              }
            }
            else
            {
LABEL_26:
              MEMORY[0x141948990](v16 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *a1 = v14;
          a1[1] = v14 + 8 * ((v9 >> 3) + 1);
          a1[2] = v14 + 8 * v13;
          a2 = v21;
          v6 = v22;
          goto LABEL_7;
        }
        *v8 = v7;
        a1[1] += 8;
      }
LABEL_7:
      ++v5;
    }
    while ( v5 != v6 );
  }
  return a1;
}
