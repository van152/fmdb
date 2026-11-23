__int64 *__fastcall sub_140FE3E30(__int64 *a1, __int64 a2)
{
  __int64 v3; // rax

  if ( a2 != 0 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)a2 + 200LL))(a2, a1);
  }
  else
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
    v3 = sub_1407E4490(&unk_141B59A68, 16);
    *(_QWORD *)(v3 + 8) = 0;
    *(_QWORD *)v3 = 0x141886BF8LL;
    *a1 = v3;
    _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
  }
  return a1;
}
