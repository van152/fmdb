__int64 *__fastcall sub_141537730(__int64 *a1, __int64 a2, char a3)
{
  __int64 v4; // rsi
  __int64 *v6; // rax
  __int64 v7; // r14
  __int64 v8; // r15
  __int64 v9; // rax
  __int64 v10; // rbx
  __int64 v11; // rdi
  __int64 *v12; // rcx
  __int64 *v13; // rdx
  __int64 v14; // rcx
  __int64 v15; // rdx
  _QWORD *v16; // rdi
  __int64 *v17; // r12
  __int64 v18; // r13
  unsigned __int64 v19; // rax
  unsigned __int64 v20; // rcx
  unsigned __int64 v21; // rax
  __int64 v22; // rsi
  _QWORD *v23; // rbx
  __int64 v24; // rdi
  unsigned __int64 v25; // rcx
  __int64 v26; // rbx
  __int64 v27; // rbx
  unsigned __int64 v29; // [rsp+20h] [rbp-20h]
  unsigned __int64 v30; // [rsp+28h] [rbp-18h]
  char v32; // [rsp+3Fh] [rbp-1h]

  v4 = a2;
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
        v4 = a2;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v6 = *(__int64 **)(qword_141B600F8 + 128);
  v7 = *v6;
  v8 = v6[1];
  if ( *v6 != v8 )
  {
    v32 = a3;
    do
    {
      v9 = *(_QWORD *)(*(_QWORD *)v7 + 32LL);
      if ( v9 != 0 )
      {
        v10 = *(_QWORD *)(*(_QWORD *)v7 + 24LL);
        if ( (*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0 )
        {
          if ( (int)v10 < 0 || qword_141B5FE10 == 0 )
            goto LABEL_7;
          if ( (_BYTE)word_141B60320 != 0
            || (v11 = *(_QWORD *)(qword_141B5FE10 + 96),
                v4 = a2,
                (*(_QWORD *)(qword_141B5FE10 + 104) - v11) >> 3 <= (unsigned __int64)(unsigned int)v10) )
          {
            v13 = *(__int64 **)(qword_141B5FE10 + 128);
            v14 = *v13;
            v15 = v13[1] - *v13;
            if ( v15 == 0 || v15 >> 3 <= (unsigned __int64)(unsigned int)v10 )
              goto LABEL_7;
            v12 = (__int64 *)(v14 + 8LL * (unsigned int)v10);
          }
          else
          {
            v12 = (__int64 *)(v11 + 8LL * (unsigned int)v10);
          }
          v10 = *v12;
        }
        if ( v10 != 0 )
        {
          if ( a3 != 0 )
          {
            if ( *(_BYTE *)(v9 + 47) != 0 || *(_QWORD *)(v9 + 48) != v4 )
              goto LABEL_7;
          }
          else if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 672LL))(v10) != v4 )
          {
            goto LABEL_7;
          }
          v16 = (_QWORD *)a1[1];
          if ( v16 == (_QWORD *)a1[2] )
          {
            v17 = a1;
            v18 = (__int64)v16 - *a1;
            v19 = (unsigned __int64)(v18 >> 3) >> 1;
            v20 = 0x1FFFFFFFFFFFFFFFLL - v19;
            v21 = (v18 >> 3) + v19;
            v29 = (v18 >> 3) + 1;
            if ( v21 <= v29 )
              v21 = (v18 >> 3) + 1;
            if ( v18 >> 3 > v20 )
              v21 = 0x1FFFFFFFFFFFFFFFLL;
            v30 = v21;
            v22 = sub_1407E4490(qword_141ABD470, 8 * v21);
            *(_QWORD *)(v22 + v18) = v10;
            v23 = (_QWORD *)v17[1];
            sub_141758A00();
            if ( v23 != v16 )
              sub_141758A00();
            v24 = *v17;
            a1 = v17;
            if ( *v17 != 0 )
            {
              v25 = v17[2] - v24;
              if ( v25 == -1 )
              {
                v25 = *(unsigned int *)(v24 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  goto LABEL_42;
              }
              else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              {
                goto LABEL_42;
              }
              v26 = *(_QWORD *)(qword_141ABD470 + 24);
              if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v25 && (v27 = *(_QWORD *)(v26 + 8 * v25)) != 0 )
              {
                MEMORY[0x1419475D8](v27 + 32, v24 - *(unsigned int *)(v27 + 120));
                if ( (*(_BYTE *)(v27 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) == 0)
                  && *(_BYTE *)(v27 + 97) != 0 )
                {
                  sub_1412D33C0(v27);
                }
              }
              else
              {
LABEL_42:
                MEMORY[0x141948990](v24 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *v17 = v22;
            v17[1] = v22 + 8 * v29;
            v17[2] = v22 + 8 * v30;
            a3 = v32;
            v4 = a2;
            goto LABEL_7;
          }
          *v16 = v10;
          a1[1] += 8;
        }
      }
LABEL_7:
      v7 += 8;
    }
    while ( v7 != v8 );
  }
  return a1;
}
