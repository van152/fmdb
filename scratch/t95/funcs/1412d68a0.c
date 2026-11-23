char __fastcall sub_1412D68A0(_QWORD *a1)
{
  char result; // al
  __int64 v3; // rcx
  __int64 v4; // rcx
  __int64 v5; // rsi
  __int64 v6; // rdi
  unsigned __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rbx
  bool v10; // al
  __int64 v11; // rdi
  signed __int32 v12; // et0

  result = -56;
  *a1 = 0x1418964C8LL;
  v3 = a1[3];
  if ( v3 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v3 + 8)) == 0 )
    result = (**(__int64 (__fastcall ***)(__int64, __int64))v3)(v3, 1);
  v4 = a1[2];
  if ( v4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 + 8)) == 0 )
    result = (**(__int64 (__fastcall ***)(__int64, __int64))v4)(v4, 1);
  v5 = a1[1];
  if ( v5 == 0 || _InterlockedDecrement((volatile signed __int32 *)v5) != 0 )
    return result;
  v6 = *(_QWORD *)(v5 + 8);
  if ( v6 != 0 )
  {
    v7 = *(_QWORD *)(v5 + 24) - v6;
    if ( v7 == -1 )
    {
      v7 = *(unsigned int *)(v6 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_18;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_18;
    }
    v8 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v8) >> 3 > v7 )
    {
      v9 = *(_QWORD *)(v8 + 8 * v7);
      if ( v9 != 0 )
      {
        MEMORY[0x1419475D8](v9 + 32, v6 - *(unsigned int *)(v9 + 120));
        v10 = *(_BYTE *)(v9 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v9 + 64)) != 0;
        if ( !v10 && *(_BYTE *)(v9 + 97) != 0 )
          sub_1412D33C0(v9);
        goto LABEL_19;
      }
    }
LABEL_18:
    MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_19:
    *(_QWORD *)(v5 + 24) = 0;
    *(_QWORD *)(v5 + 16) = 0;
    *(_QWORD *)(v5 + 8) = 0;
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
    return MEMORY[0x141948990](v5 - (unsigned int)dword_141B59A98);
  if ( (unsigned __int64)(qword_141B59A88 - qword_141B59A80) < 0x141 )
    return MEMORY[0x141948990](v5 - (unsigned int)dword_141B59A98);
  v11 = *(_QWORD *)(qword_141B59A80 + 320);
  if ( v11 == 0 )
    return MEMORY[0x141948990](v5 - (unsigned int)dword_141B59A98);
  MEMORY[0x1419475D8](v11 + 32, v5 - *(unsigned int *)(v11 + 120));
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
