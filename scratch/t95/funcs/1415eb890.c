// THUNK ALIAS -> sub_14464ADB0 (jmp:0x1415eb890->0x14464adb0)
_QWORD *__fastcall sub_14464ADB0(_QWORD *a1, __int64 a2, unsigned int a3, unsigned int a4)
{
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
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  sub_1411F7E70(a2, a3, a4, a1);
  return a1;
}
