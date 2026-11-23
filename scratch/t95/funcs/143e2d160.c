__int64 sub_143E2D160()
{
  __int64 v0; // rax
  __int64 *v1; // rsi
  __int64 v2; // rcx
  __int64 v3; // rsi
  int v5; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v6[6]; // [rsp+30h] [rbp-10h] BYREF

  v6[2] = -2;
  v0 = qword_141B60C30;
  v1 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v0 != 1214805357 )
    {
      v0 += 16;
      if ( v0 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v0 == qword_141B60C38 )
      v1 = nullptr;
    else
      v1 = *(__int64 **)(v0 + 8);
  }
LABEL_8:
  if ( v1 == nullptr )
    v1 = &qword_141B5A4A0;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v1 + 8LL * (*v1 != qword_141B5A4A0) + 32))(
         *v1,
         v1) == 0
    && (v6[1] = 0,
        v6[0] = sub_14083D4F0(v2) + 8,
        sub_140FEB270(&v5, v1),
        v3 = sub_140F8F320(&v5),
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v6[0] + 16LL))(v6[0], v6),
        v3 != 0)
    && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v3 + 56LL))(v3) == 1 )
  {
    return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 1752LL))(v3);
  }
  else
  {
    return 0;
  }
}
