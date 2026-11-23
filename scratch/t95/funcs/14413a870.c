__int64 __fastcall sub_14413A870(_QWORD *a1)
{
  *a1 = 0x141897B98LL;
  if ( dword_141B62780 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B62780);
    if ( dword_141B62780 == -1 )
    {
      sub_1412EAD20(&qword_141B62770);
      sub_141751048(sub_1412EB5A0);
      sub_141750EA0(&dword_141B62780);
    }
  }
  return sub_1412EA490(&qword_141B62770, a1 + 1);
}
