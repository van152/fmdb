__int64 __fastcall sub_140E44CE0(__int64 **a1, _QWORD *a2, __int16 a3, char a4)
{
  __int64 v8; // rbx
  __int64 *v9; // rbx
  _DWORD *v10; // rax
  __int64 *v11; // r15
  __int64 *v12; // rdi
  __int64 v13; // r14
  unsigned __int64 v14; // rax
  unsigned __int64 v15; // r12
  unsigned __int64 v16; // rdx
  unsigned __int64 v17; // r12
  __int64 v18; // rsi
  __int64 *v19; // r13
  __int64 v20; // r14
  __int64 v21; // rsi
  unsigned __int64 v22; // rcx
  __int64 v23; // rdi
  __int64 v24; // rdi
  bool v25; // al
  unsigned __int64 v27; // [rsp+48h] [rbp-8h]

  if ( (*a2 == 0 || *(_DWORD *)*a2 == 0) && (_BYTE)word_141B60460 != 6 )
    return 0;
  if ( *a1 == nullptr )
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
    v9 = (__int64 *)sub_1407E4490(&unk_141B59A68, 24);
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
    v9[2] = 0;
    v9[1] = 0;
    *v9 = 0;
    *a1 = v9;
  }
  if ( dword_141B5D8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5D8D0);
    if ( dword_141B5D8D0 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5D880, 1100152970, 1024, 16, 0, 0, 1024, 4096);
      sub_141751048(sub_140E469B0);
      sub_141750EA0(&dword_141B5D8D0);
    }
  }
  v8 = sub_1407E58C0(&unk_141B5D880, 16);
  *(_QWORD *)v8 = 0;
  if ( (_QWORD *)v8 != a2 )
  {
    v10 = (_DWORD *)*a2;
    if ( *a2 != 0 )
      _InterlockedIncrement(v10 - 1);
    *(_QWORD *)v8 = v10;
  }
  *(_WORD *)(v8 + 8) = a3;
  *(_BYTE *)(v8 + 10) = a4;
  v11 = *a1;
  v12 = (__int64 *)(*a1)[1];
  if ( v12 == (__int64 *)(*a1)[2] )
  {
    v13 = (__int64)v12 - *v11;
    v14 = v13 >> 3;
    v15 = (unsigned __int64)(v13 >> 3) >> 1;
    v16 = 0x1FFFFFFFFFFFFFFFLL - v15;
    v17 = (v13 >> 3) + v15;
    v27 = (v13 >> 3) + 1;
    if ( v17 <= v27 )
      v17 = v14 + 1;
    if ( v14 > v16 )
      v17 = 0x1FFFFFFFFFFFFFFFLL;
    v18 = sub_1407E4490(qword_141ABD470, 8 * v17);
    *(_QWORD *)(v18 + v13) = v8;
    v19 = (__int64 *)v11[1];
    sub_141758A00();
    if ( v19 != v12 )
      sub_141758A00();
    v20 = v18;
    v21 = *v11;
    if ( *v11 != 0 )
    {
      v22 = v11[2] - v21;
      if ( v22 == -1 )
        v22 = *(unsigned int *)(v21 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v23 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v23) >> 3 > v22)
        && (v24 = *(_QWORD *)(v23 + 8 * v22)) != 0 )
      {
        MEMORY[0x1419475D8](v24 + 32, v21 - *(unsigned int *)(v24 + 120));
        v25 = *(_BYTE *)(v24 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) != 0;
        if ( !v25 && *(_BYTE *)(v24 + 97) != 0 )
          sub_1412D33C0(v24);
      }
      else
      {
        MEMORY[0x141948990](v21 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *v11 = v20;
    v11[1] = v20 + 8 * v27;
    v11[2] = v20 + 8 * v17;
  }
  else
  {
    *v12 = v8;
    v11[1] += 8;
  }
  return v8;
}
