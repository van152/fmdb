// THUNK ALIAS -> sub_14475CEF0 (jmp:0x141732730->0x14475cef0)
_QWORD *__fastcall sub_14475CEF0(_QWORD *a1, _QWORD *a2, char a3)
{
  _QWORD *v6; // rax
  _QWORD *v7; // rcx
  _QWORD *v8; // rdx
  _QWORD *v9; // rdi

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
  v6 = a2 + 24;
  v7 = a2 + 25;
  v8 = a2 + 18;
  v9 = a2 + 19;
  if ( a3 == 0 )
  {
    v9 = v7;
    v8 = v6;
  }
  sub_140822710(a1, 0, *v8, (__int64)(*v9 - *v8) >> 3, -2);
  return a1;
}
