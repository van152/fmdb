__int64 __fastcall sub_14007A910(__int64 a1)
{
  __int64 v3; // rax

  if ( dword_141ABE6E0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141ABE6E0);
    if ( dword_141ABE6E0 == -1 )
    {
      v3 = sub_1407E3B90(8);
      sub_1407E4EA0((unsigned int)&unk_141ABE670, 1100125589, 10240, 24, 0, 0, 2048, v3);
      sub_141751048(sub_14007ADA0);
      sub_141750EA0(&dword_141ABE6E0);
    }
  }
  return sub_1407E5310(&unk_141ABE670, a1);
}
