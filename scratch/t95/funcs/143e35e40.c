__int64 sub_143E35E40()
{
  __int64 v0; // rax
  __int64 *v1; // rsi
  __int64 v2; // rcx
  __int64 v3; // rsi
  __int64 v4; // rax
  __int64 v5; // rcx
  int v7; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v8[6]; // [rsp+30h] [rbp-10h] BYREF

  v8[2] = -2;
  v0 = qword_141B60C30;
  v1 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v0 != 1416914273 )
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
         v1) != 0
    || (v8[1] = 0,
        v8[0] = sub_14083D4F0(v2) + 8,
        sub_140FEB270(&v7, v1),
        v3 = sub_140F8F320(&v7),
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v8[0] + 16LL))(v8[0], v8),
        v3 == 0)
    || (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v3 + 56LL))(v3) != 24
    || (_BYTE)word_141B60320 == 0 )
  {
    v4 = sub_140FE83A0();
    if ( v4 == 0 )
      return 0;
    v5 = *(_QWORD *)(v4 + 24);
    if ( v5 == *(_QWORD *)(v4 + 32) )
      return 0;
    else
      return *(_QWORD *)v5;
  }
  return v3;
}
