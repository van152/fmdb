_QWORD *__fastcall sub_143C588C0(_QWORD *a1, __int64 a2)
{
  _DWORD *v4; // rbx
  __int64 v5; // rcx
  _DWORD *v6; // rbx
  __int64 v7; // rax
  __int64 v9; // rdx
  __int64 v10; // rdx
  _BYTE v11[16]; // [rsp+20h] [rbp-20h] BYREF
  __int64 v12; // [rsp+30h] [rbp-10h]
  _DWORD *v13; // [rsp+38h] [rbp-8h]
  __int64 v14; // [rsp+40h] [rbp+0h]

  v14 = -2;
  sub_1412D5BA0(v11);
  *(_DWORD *)(v12 + 12) &= ~2u;
  v13[3] &= ~2u;
  v4 = v13;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(v13, 0x1418BD44CLL, 1);
  if ( v4[4] == 0 )
  {
    v6 = v13;
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(v13, a2, 1);
    if ( v6[4] == 0 )
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(v13, a2 + 1, 1);
  }
  v7 = sub_14083D4F0(v5);
  a1[1] = 0;
  *a1 = v7 + 8;
  if ( dword_141B59E30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59E30);
    if ( dword_141B59E30 == -1 )
    {
      byte_141B59E08 = 16;
      qword_141B59E00 = 0x14185E1D8LL;
      LOBYTE(v9) = 16;
      sub_1412EA280(&qword_141B59E10, v9);
      LOBYTE(v10) = 16;
      sub_1412EB230(&qword_141B59E20, v10);
      qword_141B59E00 = 0x14185DF88LL;
      qword_141B59E10 = 0x14185E068LL;
      qword_141B59E20 = 0x14185E088LL;
      sub_141751048(sub_140804150);
      sub_141750EA0(&dword_141B59E30);
    }
  }
  sub_140804F40(&qword_141B59E00, a1, v11);
  sub_1412D68A0(v11);
  return a1;
}
