char __fastcall sub_14106B210(__int64 a1, __int64 a2)
{
  __int64 **v3; // rax
  __int64 *v4; // rdi
  __int64 *v5; // r12
  int v6; // r13d
  char *v7; // r14
  char *v8; // r15
  __int64 v9; // rbx
  __int64 v10; // rax
  unsigned int v11; // eax
  char *v12; // r13
  __int64 v13; // r14
  unsigned __int64 v14; // r15
  unsigned __int64 v15; // rcx
  unsigned __int64 v16; // r15
  __int64 v17; // rax
  __int64 v18; // rbx
  __int64 v19; // rcx
  __int64 v20; // r14
  char result; // al
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // r13
  _DWORD *v25; // rdi
  __int64 v26; // rsi
  int v27; // r12d
  int v28; // edi
  int v29; // eax
  int v30; // r12d
  unsigned __int64 v31; // rbx
  __int64 v32; // rcx
  __int64 v33; // rsi
  signed __int32 v34; // et0
  int v35; // [rsp+28h] [rbp-48h] BYREF
  _QWORD v36[2]; // [rsp+30h] [rbp-40h] BYREF
  __int64 v37; // [rsp+40h] [rbp-30h]
  char *v38; // [rsp+48h] [rbp-28h]
  _QWORD v39[2]; // [rsp+50h] [rbp-20h] BYREF
  unsigned __int64 v40; // [rsp+60h] [rbp-10h]
  char *v41; // [rsp+68h] [rbp-8h]
  __int64 v42; // [rsp+70h] [rbp+0h]

  v42 = -2;
  v37 = a2;
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
  v3 = *(__int64 ***)(qword_141B5FDC0 + 128);
  v4 = *v3;
  v5 = v3[1];
  if ( *v3 != v5 )
  {
    v6 = 16387;
    v41 = nullptr;
    v7 = nullptr;
    v8 = nullptr;
    while ( 1 )
    {
      v9 = *v4;
      if ( *v4 != 0 )
      {
        if ( (unsigned __int8)sub_1408B4E50(v9, 0, *(_QWORD *)(*(_QWORD *)(a1 + 368) + 240LL), 0, 0) == 0 )
          goto LABEL_7;
        v10 = *(_QWORD *)(v9 + 96);
        if ( v10 != *(_QWORD *)(a1 + 368) )
          goto LABEL_7;
        if ( v10 == 0 )
          goto LABEL_7;
        v11 = *(unsigned __int8 *)(v9 + 244);
        if ( v11 > 0xE || !_bittest(&v6, v11) )
          goto LABEL_7;
        if ( v7 == v8 )
          break;
        *(_QWORD *)v7 = v9;
        v7 += 8;
      }
LABEL_7:
      if ( ++v4 == v5 )
        goto LABEL_34;
    }
    v12 = v41;
    v13 = v7 - v41;
    v14 = (unsigned __int64)(v13 >> 3) >> 1;
    v15 = 0x1FFFFFFFFFFFFFFFLL - v14;
    v16 = (v13 >> 3) + v14;
    v40 = (v13 >> 3) + 1;
    if ( v16 <= v40 )
      v16 = (v13 >> 3) + 1;
    if ( v13 >> 3 > v15 )
      v16 = 0x1FFFFFFFFFFFFFFFLL;
    v17 = sub_1407E4490(qword_141ABD470, 8 * v16);
    *(_QWORD *)(v17 + v13) = v9;
    v18 = v17;
    sub_141758A00();
    if ( v12 == nullptr )
    {
LABEL_30:
      v7 = (char *)(v18 + 8 * v40);
      v8 = (char *)(v18 + 8 * v16);
      v41 = (char *)v18;
      v6 = 16387;
      goto LABEL_7;
    }
    if ( v13 == -1 )
    {
      v13 = *(unsigned int *)&v41[-*(unsigned int *)(qword_141ABD470 + 48)];
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_29:
        MEMORY[0x141948990](&v41[-*(unsigned int *)(qword_141ABD470 + 48)]);
        goto LABEL_30;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_29;
    }
    v19 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v19) >> 3 > (unsigned __int64)v13 )
    {
      v20 = *(_QWORD *)(v19 + 8 * v13);
      if ( v20 != 0 )
      {
        MEMORY[0x1419475D8](v20 + 32, &v41[-*(unsigned int *)(v20 + 120)]);
        if ( (*(_BYTE *)(v20 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v20 + 64)) == 0)
          && *(_BYTE *)(v20 + 97) != 0 )
        {
          sub_1412D33C0(v20);
        }
        goto LABEL_30;
      }
    }
    goto LABEL_29;
  }
  v8 = nullptr;
  v7 = nullptr;
  v41 = nullptr;
LABEL_34:
  v38 = v8;
  result = sub_1408B7260(v41, v7, (v7 - v41) >> 3);
  if ( v7 == v41 )
  {
    if ( v7 == nullptr )
      return result;
  }
  else
  {
    v23 = 1;
    if ( (unsigned __int64)((v7 - v41) >> 3) >= 2 )
      v23 = (v7 - v41) >> 3;
    v40 = v23;
    v24 = 0;
    do
    {
      v25 = *(_DWORD **)&v41[8 * v24];
      if ( v25 != nullptr )
      {
        v26 = sub_14083D4F0(v22) + 8;
        v39[1] = 0;
        v39[0] = v26;
        v27 = v25[2];
        v28 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v25 + 56LL))(v25);
        (*(void (__fastcall **)(__int64, _QWORD *, _QWORD *))(*(_QWORD *)v26 + 24LL))(v26, v39, v36);
        v29 = v27 & v28;
        v30 = (v28 << 24) | v27 & 0x7FFFFF;
        if ( v29 == -1 )
          v30 = -8388609;
        v35 = v30;
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v39[0] + 16LL))(v39[0], v39);
        sub_140FEAD00(&v35, v39);
        sub_14083B5F0(v37, v39);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v39[0] + 16LL))(v39[0], v39);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v36[0] + 16LL))(v36[0], v36);
      }
      ++v24;
    }
    while ( v40 != v24 );
  }
  v31 = v38 - v41;
  if ( v38 - v41 == -1 )
  {
    v31 = *(unsigned int *)&v41[-*(unsigned int *)(qword_141ABD470 + 48)];
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      return MEMORY[0x141948990](&v41[-*(unsigned int *)(qword_141ABD470 + 48)]);
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    return MEMORY[0x141948990](&v41[-*(unsigned int *)(qword_141ABD470 + 48)]);
  }
  v32 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 <= v31 )
    return MEMORY[0x141948990](&v41[-*(unsigned int *)(qword_141ABD470 + 48)]);
  v33 = *(_QWORD *)(v32 + 8 * v31);
  if ( v33 == 0 )
    return MEMORY[0x141948990](&v41[-*(unsigned int *)(qword_141ABD470 + 48)]);
  MEMORY[0x1419475D8](v33 + 32, &v41[-*(unsigned int *)(v33 + 120)]);
  if ( *(_BYTE *)(v33 + 72) != 0 )
  {
    v34 = _InterlockedDecrement((volatile signed __int32 *)(v33 + 64));
    result = v34 != 0;
    if ( v34 != 0 )
      return result;
  }
  else
  {
    result = 0;
  }
  if ( *(_BYTE *)(v33 + 97) != 0 )
    return sub_1412D33C0(v33);
  return result;
}
