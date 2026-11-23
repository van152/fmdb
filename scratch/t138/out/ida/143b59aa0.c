__int64 __fastcall sub_143B59AA0(__int64 a1, __int16 a2)
{
  __int64 *v4; // r14
  _WORD *v5; // rbx
  __int64 v6; // rsi
  unsigned __int64 v7; // rax
  unsigned __int64 v8; // r13
  __int64 v9; // r12
  _WORD *v10; // r15
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  __int64 v13; // rbx
  __int64 v14; // rbx
  bool v15; // al
  unsigned __int64 v17; // [rsp+20h] [rbp-10h]

  v4 = *(__int64 **)(a1 + 80);
  if ( v4 == nullptr )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    v4 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
    if ( qword_141ABD470 == 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v4[2] = 0;
    v4[1] = 0;
    *v4 = 0;
    *(_QWORD *)(a1 + 80) = v4;
  }
  v5 = (_WORD *)v4[1];
  if ( v5 == (_WORD *)v4[2] )
  {
    v6 = (__int64)v5 - *v4;
    v7 = v6 >> 1;
    v8 = (v6 >> 1) + ((unsigned __int64)(v6 >> 1) >> 1);
    v17 = (v6 >> 1) + 1;
    if ( v8 <= v17 )
      v8 = v7 + 1;
    if ( v7 > (((unsigned __int64)(((__int64)v5 - *v4) >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
      v8 = 0x7FFFFFFFFFFFFFFFLL;
    v9 = sub_1407E4490(a1: qword_141ABD470, a2: 2 * v8);
    *(_WORD *)(v9 + v6) = a2;
    v10 = (_WORD *)v4[1];
    sub_141758A00(a1: v9, a2: *v4, a3: (char *)v5 - *v4);
    if ( v10 != v5 )
      sub_141758A00(a1: v9 + v6 + 2, a2: v5, a3: v4[1] - (_QWORD)v5);
    v11 = *v4;
    if ( *v4 == 0 )
      goto LABEL_25;
    v12 = v4[2] - v11;
    if ( v12 == -1 )
    {
      v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_24;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_24;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
        if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
          sub_1412D33C0(a1: v14);
        goto LABEL_25;
      }
    }
LABEL_24:
    MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_25:
    *v4 = v9;
    v4[1] = v9 + 2 * v17;
    v4[2] = v9 + 2 * v8;
    return *(_QWORD *)(*(_QWORD *)(a1 + 80) + 8LL) - 2LL;
  }
  *v5 = a2;
  v4[1] += 2;
  return *(_QWORD *)(*(_QWORD *)(a1 + 80) + 8LL) - 2LL;
}
