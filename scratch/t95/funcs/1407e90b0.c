__int64 __fastcall sub_1407E90B0(__int64 *a1, __int64 a2)
{
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rsi
  __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 *v9; // rax
  __int64 *v10; // rbx
  _QWORD v12[2]; // [rsp+28h] [rbp-28h] BYREF
  char v13[16]; // [rsp+38h] [rbp-18h] BYREF
  __int64 v14; // [rsp+48h] [rbp-8h]

  v14 = -2;
  v4 = sub_1407E8EB0();
  if ( v4 == 0 )
    return 0;
  v5 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v4 + 8LL))(v4, a2);
  v6 = v5 - 8;
  if ( v5 == 0 )
    return 0;
  v7 = *a1;
  v8 = a1[1];
  v9 = nullptr;
  if ( *a1 != v8 )
  {
    while ( *(_DWORD *)v7 != 1886547824 )
    {
      v7 += 16;
      if ( v7 == v8 )
        goto LABEL_11;
    }
    if ( v7 == v8 )
      v9 = nullptr;
    else
      v9 = *(__int64 **)(v7 + 8);
  }
LABEL_11:
  v10 = &qword_141B5A4A0;
  if ( v9 != nullptr )
    v10 = v9;
  sub_1412D5BA0(v12);
  sub_140805400(v10, v12);
  *(_DWORD *)(v12[1] + 32LL) = 0;
  (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)(v6 + 8) + 24LL))(v6 + 8, v13);
  sub_1412D68A0(v12);
  return v6;
}
