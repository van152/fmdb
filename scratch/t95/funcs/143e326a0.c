_QWORD *__fastcall sub_143E326A0(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v7; // rdx
  __int64 v8; // rdx
  _BYTE v9[16]; // [rsp+28h] [rbp-28h] BYREF
  __int64 v10; // [rsp+38h] [rbp-18h]
  _QWORD v11[4]; // [rsp+40h] [rbp-10h] BYREF

  v11[1] = -2;
  sub_1412D5BA0(v9);
  *(_DWORD *)(v10 + 12) &= ~2u;
  *(_DWORD *)(v11[0] + 12LL) &= ~2u;
  sub_14151C050(a2, v11);
  v5 = sub_14083D4F0(v4);
  a1[1] = 0;
  *a1 = v5 + 8;
  if ( dword_141B59E30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59E30);
    if ( dword_141B59E30 == -1 )
    {
      byte_141B59E08 = 16;
      qword_141B59E00 = 0x14185E1D8LL;
      LOBYTE(v7) = 16;
      sub_1412EA280(&qword_141B59E10, v7);
      LOBYTE(v8) = 16;
      sub_1412EB230(&qword_141B59E20, v8);
      qword_141B59E00 = 0x14185DF88LL;
      qword_141B59E10 = 0x14185E068LL;
      qword_141B59E20 = 0x14185E088LL;
      sub_141751048(sub_140804150);
      sub_141750EA0(&dword_141B59E30);
    }
  }
  sub_140804F40(&qword_141B59E00, a1, v9);
  sub_1412D68A0(v9);
  return a1;
}
