__int64 __fastcall sub_1408FF7F0(__int64 a1, __int64 a2, char a3)
{
  __int64 v3; // r14
  __int64 v4; // rsi
  __int64 v5; // r15
  char *v6; // rbx
  char *v7; // r10
  char *v8; // r11
  unsigned __int64 v9; // r13
  __int64 v10; // rbx
  unsigned __int64 v11; // r14
  unsigned __int64 v12; // r12
  unsigned __int64 v13; // rcx
  unsigned __int64 v14; // r12
  char *v15; // rsi
  __int64 v16; // rdi
  __int64 v17; // rcx
  __int64 v18; // rbx
  char *v19; // rcx
  __int64 v20; // rdx
  __int16 v21; // di
  int v22; // esi
  int v23; // edi
  int v24; // r9d
  int v25; // r8d
  unsigned __int16 v26; // di
  bool v27; // cc
  unsigned __int64 v28; // r10
  __int64 v29; // rdx
  __int64 v30; // rsi
  bool v31; // al
  __int64 v33; // [rsp+20h] [rbp-10h]
  __int64 v34; // [rsp+28h] [rbp-8h]

  if ( a2 == 0 )
    a2 = *(_QWORD *)(a1 + 288);
  v3 = *(_QWORD *)(a2 + 168);
  if ( a3 == 0 || a2 != *(_QWORD *)(a1 + 288) )
    return v3;
  v4 = a1;
  v34 = *(_QWORD *)(a2 + 168);
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
  v5 = *(_QWORD *)(v4 + 296);
  if ( *(_QWORD *)(v4 + 304) == v5 )
    return v34;
  v6 = nullptr;
  v7 = nullptr;
  v8 = nullptr;
  v9 = 0;
  v33 = v4;
  do
  {
    if ( v6 != v7 )
    {
      *(_QWORD *)v6 = *(_QWORD *)(v5 + 8 * v9);
      v6 += 8;
      goto LABEL_11;
    }
    v10 = v6 - v8;
    v11 = (v10 >> 3) + 1;
    v12 = (unsigned __int64)(v10 >> 3) >> 1;
    v13 = 0x1FFFFFFFFFFFFFFFLL - v12;
    v14 = (v10 >> 3) + v12;
    if ( v14 <= v11 )
      v14 = (v10 >> 3) + 1;
    if ( v10 >> 3 > v13 )
      v14 = 0x1FFFFFFFFFFFFFFFLL;
    v15 = v8;
    v16 = sub_1407E4490(qword_141ABD470, 8 * v14);
    *(_QWORD *)(v16 + v10) = *(_QWORD *)(v5 + 8 * v9);
    sub_141758A00();
    if ( v15 != nullptr )
    {
      if ( v10 == -1 )
      {
        v10 = *(unsigned int *)&v15[-*(unsigned int *)(qword_141ABD470 + 48)];
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_27:
          MEMORY[0x141948990](&v15[-*(unsigned int *)(qword_141ABD470 + 48)]);
          goto LABEL_28;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_27;
      }
      v17 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > (unsigned __int64)v10 )
      {
        v18 = *(_QWORD *)(v17 + 8 * v10);
        if ( v18 != 0 )
        {
          MEMORY[0x1419475D8](v18 + 32, &v15[-*(unsigned int *)(v18 + 120)]);
          if ( (*(_BYTE *)(v18 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) == 0)
            && *(_BYTE *)(v18 + 97) != 0 )
          {
            sub_1412D33C0(v18);
          }
          goto LABEL_28;
        }
      }
      goto LABEL_27;
    }
LABEL_28:
    v6 = (char *)(v16 + 8 * v11);
    v7 = (char *)(v16 + 8 * v14);
    v8 = (char *)v16;
    v4 = v33;
LABEL_11:
    ++v9;
    v5 = *(_QWORD *)(v4 + 296);
  }
  while ( v9 < (*(_QWORD *)(v4 + 304) - v5) >> 3 );
  if ( v8 != v6 )
  {
    v19 = v8;
    v3 = v34;
    while ( 1 )
    {
      v20 = *(_QWORD *)(*(_QWORD *)v19 + 168LL);
      if ( v20 == 0 || *(_QWORD *)(v20 + 72) == 0 )
        goto LABEL_35;
      if ( v3 != 0 )
      {
        v21 = *(_WORD *)(v20 + 86);
        if ( *(_WORD *)(v3 + 86) != 0 )
        {
          if ( v21 == 0 )
            goto LABEL_35;
LABEL_41:
          v22 = HIWORD(*(_DWORD *)(v3 + 80));
          v23 = *(_DWORD *)(v3 + 80) & 0x1FF;
          if ( v22 == 1900 && (_WORD)v23 == 1
            || (v24 = HIWORD(*(_DWORD *)(v20 + 80)), v25 = *(_DWORD *)(v20 + 80) & 0x1FF, v24 == 1900)
            && (_WORD)v25 == 1
            || (_WORD)v22 == (_WORD)v24 && (_WORD)v23 == (_WORD)v25 )
          {
            v26 = *(_WORD *)(v20 + 84);
            v27 = *(_WORD *)(v3 + 84) < v26;
            if ( *(_WORD *)(v3 + 84) == v26 )
              v27 = *(_BYTE *)(v3 + 94) < *(_BYTE *)(v20 + 94);
            if ( !v27 )
              goto LABEL_35;
          }
          else if ( (unsigned __int16)v22 >= (unsigned __int16)v24
                 && ((unsigned __int16)v22 > (unsigned __int16)v24 || (unsigned __int16)v23 >= (unsigned __int16)v25) )
          {
            goto LABEL_35;
          }
          goto LABEL_34;
        }
        if ( v21 == 0 )
          goto LABEL_41;
      }
LABEL_34:
      v3 = *(_QWORD *)(*(_QWORD *)v19 + 168LL);
LABEL_35:
      v19 += 8;
      if ( v19 == v6 )
        goto LABEL_57;
    }
  }
  v3 = v34;
LABEL_57:
  if ( v8 != nullptr )
  {
    v28 = v7 - v8;
    if ( v28 == -1 )
    {
      v28 = *(unsigned int *)&v8[-*(unsigned int *)(qword_141ABD470 + 48)];
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_66;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_66;
    }
    v29 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28 && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
    {
      MEMORY[0x1419475D8](v30 + 32, &v8[-*(unsigned int *)(v30 + 120)]);
      v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
      if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
        sub_1412D33C0(v30);
    }
    else
    {
LABEL_66:
      MEMORY[0x141948990](&v8[-*(unsigned int *)(qword_141ABD470 + 48)]);
    }
  }
  return v3;
}
