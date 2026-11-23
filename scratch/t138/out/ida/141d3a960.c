char __fastcall sub_141D3A960(__int64 a1, unsigned int a2)
{
  void (__fastcall ***v4)(_QWORD, __int64); // rcx
  __int64 v5; // rax
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v8; // [rsp+58h] [rbp-E0h] BYREF
  __int64 v9; // [rsp+60h] [rbp-D8h] BYREF
  _BYTE v10[8]; // [rsp+68h] [rbp-D0h] BYREF
  _BYTE v11[8]; // [rsp+70h] [rbp-C8h] BYREF
  _BYTE v12[8]; // [rsp+78h] [rbp-C0h] BYREF
  _BYTE v13[32]; // [rsp+80h] [rbp-B8h] BYREF
  _QWORD v14[7]; // [rsp+A0h] [rbp-98h] BYREF
  _BYTE v15[16]; // [rsp+D8h] [rbp-60h] BYREF
  _BYTE v16[80]; // [rsp+E8h] [rbp-50h] BYREF

  sub_140823B40(a1: qword_141ABD468, a2: v13, a3: 292655);
  sub_140048080(a1: &v8);
  if ( (_BYTE)a2 == 0 )
  {
    sub_1407D5DC0(a1: qword_141ABD878, a2: v14, a3: &qword_141B59838);
    v4 = (void (__fastcall ***)(_QWORD, __int64))v8;
    if ( v8 == v14[0] )
    {
      if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
        (**v4)(a1: v4, a2: 1);
    }
    else
    {
      if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
        (**v4)(a1: v4, a2: 1);
      v8 = v14[0];
    }
  }
  if ( v8 != 0 )
  {
    sub_1407C9510(a1: v16);
    sub_14083D9C0(a1: v14, a2: 0x1418DD169LL);
    sub_140835380(a1: v16, a2: 1953068140, a3: v14);
    sub_14083D320(a1: v14);
    sub_140146740(a1: v14, a2: 1937138534, a3: 0);
    sub_14083D6D0(a1: v15, a2);
    sub_140835380(a1: v14, a2: 1684152352, a3: v15);
    sub_14083D320(a1: v15);
    sub_1407D8AB0(a1: v12, a2: 0x1418E2C24LL);
    v5 = sub_140179440(a1: v12);
    sub_1407D8AC0(a1: v15, a2: v5);
    v9 = 0;
    sub_140809040(a1: &v9, a2: 0x1419435F1LL, a3: 0xFFFFFFFFLL);
    sub_1407D5F40(a1: v11, a2: &v9);
    sub_14081ED40(a1: v13, a2: v10, a3: 0);
    sub_14016F990(
      a1,
      a2: *(_QWORD *)(a1 + 72),
      a3: (unsigned int)v10,
      a4: (unsigned int)&v8,
      a5: (__int64)v11,
      a6: (__int64)v15,
      a7: (__int64)v14,
      a8: (unsigned int)&qword_141B59EE0,
      a9: 0,
      a10: (__int64)v16);
    sub_140808B00(a1: v10);
    sub_140808B00(a1: v11);
    sub_140808B00(a1: &v9);
    sub_140833970(a1: v14);
    sub_140833970(a1: v16);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v8;
    if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  sub_14081D040(a1: v13);
  return 1;
}
