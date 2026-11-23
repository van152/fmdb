__int64 *__fastcall sub_140828EC0(__int64 *a1, __int64 *a2)
{
  __int64 v3; // rdi
  __int64 v4; // rax

  v3 = *a2;
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
  v4 = sub_1407E4490(&unk_141B59A68, 32);
  *(_DWORD *)(v4 + 8) = 0;
  *(_DWORD *)(v4 + 16) = 0;
  *(_QWORD *)v4 = 0x14185F398LL;
  *(_QWORD *)(v4 + 24) = v3;
  *a1 = v4;
  _InterlockedIncrement((volatile signed __int32 *)(v4 + 8));
  return a1;
}
