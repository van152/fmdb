__int64 __fastcall sub_143E3FC60(__int64 a1)
{
  _QWORD **v2; // rax
  _QWORD *v3; // rax
  __int64 v4; // rdi
  __int64 v5; // rdi

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
  v2 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(***(_QWORD ***)(a1 + 8) + 96LL))(**(_QWORD **)(a1 + 8));
  if ( v2 != nullptr )
  {
    v3 = *v2;
    if ( v3 != nullptr )
    {
      v4 = v3[1] - *v3;
      if ( v4 != 0 )
      {
        v5 = v4 >> 3;
        do
        {
          (*(void (__fastcall **)(_QWORD))(***(_QWORD ***)(a1 + 8) + 96LL))(**(_QWORD **)(a1 + 8));
          --v5;
        }
        while ( v5 != 0 );
      }
    }
  }
  return off_141AB7D90();
}
