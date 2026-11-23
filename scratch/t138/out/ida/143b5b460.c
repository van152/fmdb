_QWORD *__fastcall sub_143B5B460(_QWORD *a1)
{
  _QWORD *v2; // rax

  if ( dword_141B5CA60 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5CA60);
    if ( dword_141B5CA60 == -1 )
    {
      sub_1407E53D0(a1: (unsigned int)&unk_141B5CA10, a2: 1100159964, a3: 256, a4: 32, a5: 0, a6: 0, a7: 256, a8: 4096);
      sub_141751048(a1: sub_140DD5680);
      sub_141750EA0(a1: &dword_141B5CA60);
    }
  }
  v2 = (_QWORD *)sub_1407E58C0(a1: &unk_141B5CA10, a2: 32);
  v2[3] = 124518401;
  *v2 = 0x141877B08LL;
  v2[1] = -1;
  v2[2] = 0x76C0001076C0001LL;
  *a1 = v2;
  return a1;
}
