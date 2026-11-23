char __fastcall sub_143BFA490(__int64 ****a1)
{
  __int64 ***v1; // r14
  __int64 **v2; // r15
  __int64 **v3; // rdi
  __int64 **v4; // rbx
  __int64 *v5; // rsi
  __int64 v6; // rcx
  __int64 v7; // rsi
  unsigned __int64 v8; // rcx
  __int64 v9; // rdx
  __int64 v10; // rbx
  __int64 v11; // rdi
  signed __int32 v12; // et0
  char result; // al

  v1 = *a1;
  if ( *a1 == nullptr )
    return result;
  v2 = *v1;
  v3 = v1[1];
  if ( *v1 != v3 )
  {
    v4 = *v1;
    do
    {
      v5 = *v4;
      if ( *v4 != nullptr )
      {
        v6 = *v5;
        if ( *v5 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 - 4)) == 0 )
          sub_1412EC9A0(v6 - 4);
        sub_140E469C0(v5);
      }
      ++v4;
    }
    while ( v4 != v3 );
    v7 = (char *)v1[1] - (char *)v3;
    sub_141758A00();
    v1[1] = (__int64 **)((char *)v2 + v7);
    v3 = *v1;
  }
  if ( v3 != nullptr )
  {
    v8 = (char *)v1[2] - (char *)v3;
    if ( v8 == -1 )
    {
      v8 = *(unsigned int *)((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_21;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_21;
    }
    v9 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 > v8 )
    {
      v10 = *(_QWORD *)(v9 + 8 * v8);
      if ( v10 != 0 )
      {
        MEMORY[0x1419475D8](v10 + 32, (char *)v3 - *(unsigned int *)(v10 + 120));
        if ( (*(_BYTE *)(v10 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v10 + 64)) == 0)
          && *(_BYTE *)(v10 + 97) != 0 )
        {
          sub_1412D33C0(v10);
        }
        goto LABEL_22;
      }
    }
LABEL_21:
    MEMORY[0x141948990]((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_22:
    v1[2] = nullptr;
    v1[1] = nullptr;
    *v1 = nullptr;
  }
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
  if ( byte_141B59A9C == 0 )
    return MEMORY[0x141948990]((char *)v1 - (unsigned int)dword_141B59A98);
  if ( (unsigned __int64)(qword_141B59A88 - qword_141B59A80) < 0xC1 )
    return MEMORY[0x141948990]((char *)v1 - (unsigned int)dword_141B59A98);
  v11 = *(_QWORD *)(qword_141B59A80 + 192);
  if ( v11 == 0 )
    return MEMORY[0x141948990]((char *)v1 - (unsigned int)dword_141B59A98);
  MEMORY[0x1419475D8](v11 + 32, (char *)v1 - *(unsigned int *)(v11 + 120));
  if ( *(_BYTE *)(v11 + 72) != 0 )
  {
    v12 = _InterlockedDecrement((volatile signed __int32 *)(v11 + 64));
    result = v12 != 0;
    if ( v12 != 0 )
      return result;
  }
  else
  {
    result = 0;
  }
  if ( *(_BYTE *)(v11 + 97) != 0 )
    return sub_1412D33C0(v11);
  return result;
}
