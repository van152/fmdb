__int64 __fastcall sub_144139F30(_QWORD *a1)
{
  *a1 = 0x141897B58LL;
  if ( dword_141B62768 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B62768);
    if ( dword_141B62768 == -1 )
    {
      sub_1412EAD20(&qword_141B62758);
      sub_141751048(sub_1412EAE20);
      sub_141750EA0(&dword_141B62768);
    }
  }
  return sub_1412EA490(&qword_141B62758, a1 + 1);
}
