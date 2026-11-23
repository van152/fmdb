__int64 __fastcall sub_1400039E0(__int64 a1)
{
  __int64 result; // rax
  __int64 v3; // rax

  result = (unsigned int)dword_141ABD750;
  if ( dword_141ABD750 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141ABD750);
    if ( dword_141ABD750 == -1 )
    {
      v3 = sub_1407E3B90(8);
      sub_1407E4EA0((unsigned int)&unk_141ABD6E0, 1100151682, 0x4000, 16, 0, 0, 4096, v3);
      sub_141751048(sub_140003AA0);
      result = sub_141750EA0(&dword_141ABD750);
    }
  }
  if ( a1 != 0 )
    return sub_1407E5380(&unk_141ABD6E0, a1);
  return result;
}
