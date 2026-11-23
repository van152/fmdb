char __fastcall sub_143FCDAB0(__int64 a1, int a2, _QWORD *a3)
{
  unsigned int v6; // eax
  __int64 v7; // rdx
  __int64 v8; // rdx
  int v9; // [rsp+20h] [rbp-28h] BYREF
  _BYTE v10[32]; // [rsp+28h] [rbp-20h] BYREF

  if ( a2 == 1684108389 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        qword_141B5C8A0 = 0x141759DF8LL;
        byte_141B5C8A8 = 32;
        LOBYTE(v7) = 32;
        sub_1412EA280(&qword_141B5C8B0, v7);
        LOBYTE(v8) = 32;
        sub_1412EB230(&qword_141B5C8C0, v8);
        qword_141B5C8A0 = 0x141876208LL;
        qword_141B5C8B0 = 0x1418762E8LL;
        qword_141B5C8C0 = 0x141876308LL;
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    if ( (__int64 *)*a3 == &qword_141B5C8A0 )
    {
      v6 = *((_DWORD *)a3 + 2);
      HIWORD(v9) = v6 >> 17;
      LOWORD(v9) = (v6 >> 8) & 0x1FF | ((_WORD)v6 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
    {
      (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v10, a3);
      sub_1413CA830(&v9, v10);
    }
    else
    {
      v9 = 124518401;
    }
    *(_DWORD *)(a1 + 32) = v9;
  }
  else
  {
    if ( a2 != 1954115685 )
      return 0;
    *(_BYTE *)(a1 + 36) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  }
  return 1;
}
