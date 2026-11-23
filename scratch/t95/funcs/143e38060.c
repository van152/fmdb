__int64 sub_143E38060()
{
  __int64 v0; // rax
  __int64 *v1; // rsi
  __int64 v2; // rcx
  __int64 v3; // rsi
  int v4; // ecx
  __int64 result; // rax
  int v6; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v7[6]; // [rsp+30h] [rbp-10h] BYREF

  v7[2] = -2;
  v0 = qword_141B60C30;
  v1 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v0 != 1130589301 )
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
         v1) != 0 )
    return 0;
  v7[1] = 0;
  v7[0] = sub_14083D4F0(v2) + 8;
  sub_140FEB270(&v6, v1);
  v3 = sub_140F8F320(&v6);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v7[0] + 16LL))(v7[0], v7);
  if ( v3 == 0 )
    return 0;
  v4 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 56LL))(v3);
  result = 0;
  if ( v4 == 3 )
    return v3;
  return result;
}
