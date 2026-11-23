__int64 __fastcall sub_1443F10B0(__int64 a1, int *a2)
{
  __int64 v3; // rdx
  int v4; // eax
  __int64 v5; // rcx
  int v6; // edi
  __int64 *v7; // rsi
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rcx
  __int64 v12; // rdx
  __int64 v13; // rdx
  __int64 *v14; // [rsp+28h] [rbp-28h] BYREF
  unsigned int v15; // [rsp+30h] [rbp-20h]
  __int64 v16; // [rsp+38h] [rbp-18h] BYREF
  __int64 v17; // [rsp+40h] [rbp-10h]
  __int64 v18; // [rsp+48h] [rbp-8h]

  v18 = -2;
  if ( a1 != 0 )
  {
    v3 = *(_QWORD *)(a1 + 8);
    v4 = 890241023;
    if ( v3 != 0
      && qword_141B5FE08 != 0
      && **(_QWORD **)(qword_141B5FE08 + 128) != *(_QWORD *)(*(_QWORD *)(qword_141B5FE08 + 128) + 8LL) )
    {
      v4 = *(_DWORD *)(v3 + 8) & 0x7FFFFF | 0x35000000;
    }
    *a2 = v4;
    v5 = a1 + 76;
  }
  else
  {
    *a2 = 890241023;
    v5 = 0x1418761ECLL;
  }
  v6 = *(_DWORD *)v5;
  if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5C8D0);
    if ( dword_141B5C8D0 == -1 )
    {
      qword_141B5C8A0 = 0x141759DF8LL;
      byte_141B5C8A8 = 32;
      LOBYTE(v12) = 32;
      sub_1412EA280(&qword_141B5C8B0, v12);
      LOBYTE(v13) = 32;
      sub_1412EB230(&qword_141B5C8C0, v13);
      qword_141B5C8A0 = 0x141876208LL;
      qword_141B5C8B0 = 0x1418762E8LL;
      qword_141B5C8C0 = 0x141876308LL;
      sub_141751048(sub_140DBCA10);
      sub_141750EA0(&dword_141B5C8D0);
    }
  }
  v15 = (v6 << 8) & 0x1FF00 | (((unsigned __int16)v6 >> 9) + 2 * (v6 & 0xFFFF0000));
  v14 = &qword_141B5C8A0;
  (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(qword_141B5C8A0 + 24))(&qword_141B5C8A0, &v14, &v16);
  v7 = (__int64 *)(a2 + 2);
  if ( v7 == &v16 )
  {
    v10 = v16;
  }
  else
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v7 + 16LL))(*v7, v7);
    v8 = v16;
    v9 = v17;
    v7[1] = v17;
    *v7 = v8;
    v10 = sub_14083D4F0(v9) + 8;
    v17 = 0;
    v16 = v10;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v10 + 16LL))(v10, &v16);
  return (*(__int64 (__fastcall **)(__int64 *, __int64 **))(*v14 + 16))(v14, &v14);
}
