// THUNK ALIAS -> sub_143EC6FE0 (jmp:0x14103fbf0->0x143ec6fe0)
__int64 *__fastcall sub_143EC6FE0(__int64 a1, __int64 *a2)
{
  __int64 v4; // rdi
  _QWORD *v6; // rax

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
  v4 = sub_1407E4490(&unk_141B59A68, 24);
  *(_DWORD *)(v4 + 8) = 0;
  *(_QWORD *)(v4 + 16) = a1;
  *(_QWORD *)v4 = 0x1418C4178LL;
  if ( dword_141ABFB88 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141ABFB88);
    if ( dword_141ABFB88 == -1 )
    {
      v6 = (_QWORD *)sub_141750CC0(8);
      *v6 = 0x14176BFB8LL;
      qword_141ABFB78 = (__int64)v6;
      byte_141ABFB80 = 0;
      sub_141751048(sub_140103BF0);
      sub_141750EA0(&dword_141ABFB88);
    }
  }
  if ( byte_141ABFB80 == 0 )
  {
    (*(void (__fastcall **)(__int64))(*(_QWORD *)qword_141ABFB78 + 64LL))(qword_141ABFB78);
    byte_141ABFB80 = 1;
  }
  *a2 = v4;
  _InterlockedIncrement((volatile signed __int32 *)(v4 + 8));
  return a2;
}
