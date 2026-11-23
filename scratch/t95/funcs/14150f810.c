__int64 __fastcall sub_14150F810(__int64 a1)
{
  _QWORD v3[5]; // [rsp+28h] [rbp-18h] BYREF

  v3[2] = -2;
  v3[1] = 0;
  v3[0] = sub_14083D4F0(a1) + 8;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v3[0] + 24LL))(v3[0], v3, a1 + 8);
  *(_DWORD *)a1 = -8388609;
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v3[0] + 16LL))(v3[0], v3);
  if ( qword_141ABD470 == 0 )
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
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_QWORD *)(a1 + 46) = 0;
  *(_QWORD *)(a1 + 40) = 0;
  *(_QWORD *)(a1 + 32) = 0;
  *(_QWORD *)(a1 + 24) = 0;
  *(_QWORD *)(a1 + 56) = 0;
  *(_QWORD *)(a1 + 64) = 0;
  *(_QWORD *)(a1 + 72) = 0;
  *(_QWORD *)(a1 + 77) = 0;
  return a1;
}
