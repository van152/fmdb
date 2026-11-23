void __fastcall sub_14372DF10(__int64 *a1)
{
  __int64 v2; // rdi
  __int64 v3; // rbx
  __int64 v4; // rbx
  __int64 v5; // rcx
  __int64 v6; // rdi
  __int64 v7; // rcx

  v2 = a1[2];
  if ( v2 != 0 )
  {
    sub_14081D260(a1[2]);
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
    if ( byte_141B59A9C != 0
      && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
      && (v3 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
    {
      MEMORY[0x1419475D8](v3 + 32, v2 - *(unsigned int *)(v3 + 120));
      if ( (*(_BYTE *)(v3 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v3 + 64)) == 0)
        && *(_BYTE *)(v3 + 97) != 0 )
      {
        sub_1412D33C0(v3);
      }
    }
    else
    {
      MEMORY[0x141948990](v2 - (unsigned int)dword_141B59A98);
    }
  }
  v4 = *a1;
  if ( *a1 != 0 && *((_DWORD *)a1 + 6) == -1 )
  {
    sub_1413133F0(*a1);
    v6 = sub_14081FDA0(v5);
    MEMORY[0x1419475D8](v6 + 32, v4);
    if ( (*(_BYTE *)(v6 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v6 + 64)) == 0)
      && *(_BYTE *)(v6 + 97) != 0 )
    {
      sub_1412D33C0(v6);
    }
  }
  v7 = a1[1];
  if ( v7 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7 - 4)) == 0 )
    sub_1412EC9A0(v7 - 4);
}
