// THUNK ALIAS -> sub_14420D310 (jmp:0x141335f60->0x14420d310)
__int64 *sub_14420D310()
{
  if ( dword_141B62F80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B62F80);
    if ( dword_141B62F80 == -1 )
    {
      sub_141336010(&qword_141B62F50);
      sub_141751048(sub_1413360A0);
      sub_141750EA0(&dword_141B62F80);
    }
  }
  return &qword_141B62F50;
}
