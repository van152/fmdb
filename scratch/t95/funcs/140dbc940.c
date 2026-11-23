// THUNK ALIAS -> sub_143B53130 (jmp:0x140dbc940->0x143b53130)
__int64 *sub_143B53130()
{
  if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5C8D0);
    if ( dword_141B5C8D0 == -1 )
    {
      sub_140DBC9B0(&qword_141B5C8A0);
      sub_141751048(sub_140DBCA10);
      sub_141750EA0(&dword_141B5C8D0);
    }
  }
  return &qword_141B5C8A0;
}
