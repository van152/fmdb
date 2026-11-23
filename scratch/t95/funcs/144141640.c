char __fastcall sub_144141640(__int64 a1)
{
  char result; // al
  unsigned int *v3; // rcx
  unsigned __int64 v4; // rax
  __int64 v5; // rdi
  signed __int32 v6; // et0

  result = dword_141B627C8;
  if ( dword_141B627C8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B627C8);
    if ( dword_141B627C8 == -1 )
    {
      sub_1412ECB10(&unk_141B62788);
      sub_141751048(sub_1412ECD20);
      result = sub_141750EA0(&dword_141B627C8);
    }
  }
  if ( a1 != 0 )
  {
    v3 = (unsigned int *)(a1 - (unsigned int)dword_141B627B8);
    if ( byte_141B627BC == 0 )
      return MEMORY[0x141948990](v3);
    v4 = *v3;
    if ( (qword_141B627A8 - qword_141B627A0) >> 3 <= v4 )
      return MEMORY[0x141948990](v3);
    v5 = *(_QWORD *)(qword_141B627A0 + 8 * v4);
    if ( v5 == 0 )
      return MEMORY[0x141948990](v3);
    MEMORY[0x1419475D8](v5 + 32, a1 - *(unsigned int *)(v5 + 120));
    if ( *(_BYTE *)(v5 + 72) != 0 )
    {
      v6 = _InterlockedDecrement((volatile signed __int32 *)(v5 + 64));
      result = v6 != 0;
      if ( v6 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v5 + 97) != 0 )
      return sub_1412D33C0(v5);
  }
  return result;
}
