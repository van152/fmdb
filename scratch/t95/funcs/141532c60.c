__int64 *__fastcall sub_141532C60(__int64 *a1, __int64 a2, char a3)
{
  __int64 v6; // rax
  unsigned __int64 v7; // r13
  _QWORD *v8; // rdi
  __int64 v9; // r14
  _QWORD *v10; // rax
  __int64 v11; // rdx
  __int64 *v12; // r15
  __int64 v13; // r12
  unsigned __int64 v14; // rax
  unsigned __int64 v15; // rdi
  __int64 v16; // rbx
  __int64 *v17; // r14
  __int64 v18; // r15
  __int64 v19; // rbx
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // r14
  char v24; // [rsp+4Fh] [rbp-1h] BYREF
  __int64 v25; // [rsp+50h] [rbp+0h]

  v25 = -2;
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
  a1[3] = a2;
  a1[4] = 0;
  *((_BYTE *)a1 + 40) = a3;
  if ( a3 != 0 )
  {
    v6 = *(_QWORD *)(a2 + 280);
    if ( *(_QWORD *)(a2 + 288) != v6 )
    {
      v7 = 0;
      while ( 1 )
      {
        v8 = *(_QWORD **)(v6 + 8 * v7);
        if ( v8 == nullptr )
          goto LABEL_9;
        v9 = sub_141750CC0(16);
        if ( dword_141B5ED18 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5ED18);
          if ( dword_141B5ED18 == -1 )
          {
            sub_1407E53D0((unsigned int)&unk_141B5ECC8, 1100148257, 64, 56, 0, 0, 64, 4096);
            sub_141751048(sub_140FB3890);
            sub_141750EA0(&dword_141B5ED18);
          }
        }
        v10 = (_QWORD *)sub_1407E58C0(&unk_141B5ECC8, 56);
        v11 = v8[1];
        *v10 = *v8;
        v10[1] = v11;
        v10[2] = v8[2];
        v10[3] = v8[3];
        v10[4] = v8[4];
        v10[5] = v8[5];
        v10[6] = v8[6];
        *(_QWORD *)v9 = v10;
        *(_BYTE *)(v9 + 8) = 0;
        v24 = 0;
        sub_141528E60(v10, &v24, 0, 0);
        *(_BYTE *)(v9 + 8) = v24;
        v12 = (__int64 *)a1[1];
        if ( v12 == (__int64 *)a1[2] )
          break;
        *v12 = v9;
        a1[1] += 8;
LABEL_8:
        a2 = a1[3];
LABEL_9:
        ++v7;
        v6 = *(_QWORD *)(a2 + 280);
        if ( v7 >= (*(_QWORD *)(a2 + 288) - v6) >> 3 )
          return a1;
      }
      v13 = (__int64)v12 - *a1;
      v14 = v13 >> 3;
      v15 = v14 + (v14 >> 1);
      if ( v15 <= (v13 >> 3) + 1 )
        v15 = v14 + 1;
      if ( v14 > 0x1FFFFFFFFFFFFFFFLL - (v14 >> 1) )
        v15 = 0x1FFFFFFFFFFFFFFFLL;
      v16 = sub_1407E4490(qword_141ABD470, 8 * v15);
      *(_QWORD *)(v16 + v13) = v9;
      v17 = (__int64 *)a1[1];
      sub_141758A00();
      if ( v17 != v12 )
        sub_141758A00();
      v18 = v16;
      v19 = *a1;
      if ( *a1 == 0 )
      {
LABEL_30:
        *a1 = v18;
        a1[1] = v18 + 8 * ((v13 >> 3) + 1);
        a1[2] = v18 + 8 * v15;
        goto LABEL_8;
      }
      v20 = a1[2] - v19;
      if ( v20 == -1 )
      {
        v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_29:
          MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_30;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_29;
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
          goto LABEL_30;
        }
      }
      goto LABEL_29;
    }
  }
  return a1;
}
