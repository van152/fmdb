char __fastcall sub_141D3A690(__int64 a1)
{
  __int64 v2; // rax
  void (__fastcall ***v3)(_QWORD, __int64); // rcx
  __int64 v5; // [rsp+48h] [rbp-D0h] BYREF
  __int64 v6; // [rsp+50h] [rbp-C8h] BYREF
  _BYTE v7[8]; // [rsp+58h] [rbp-C0h] BYREF
  _BYTE v8[8]; // [rsp+60h] [rbp-B8h] BYREF
  _BYTE v9[24]; // [rsp+68h] [rbp-B0h] BYREF
  _BYTE v10[56]; // [rsp+80h] [rbp-98h] BYREF
  _BYTE v11[96]; // [rsp+B8h] [rbp-60h] BYREF

  v6 = 0;
  sub_140809040(a1: &v6, a2: 0x14191DA30LL, a3: 0xFFFFFFFFLL);
  sub_140048080(a1: &v5);
  if ( v5 != 0 )
  {
    sub_1407C9510(a1: v9);
    sub_14083D9C0(a1: v11, a2: 0x1418DD191LL);
    sub_140835380(a1: v9, a2: 1953068140, a3: v11);
    sub_14083D320(a1: v11);
    sub_140146740(a1: v11, a2: 1818518374, a3: 0);
    sub_140146740(a1: v10, a2: 1313820229, a3: 0);
    sub_1407D8AB0(a1: v7, a2: 0x1418E2C24LL);
    v2 = sub_140179440(a1: v7);
    sub_1407D8AC0(a1: v8, a2: v2);
    sub_14016F5F0(
      a1,
      a2: *(_QWORD *)(a1 + 72),
      a3: (unsigned int)&v6,
      a4: (unsigned int)&v5,
      a5: (__int64)v8,
      a6: (__int64)v11,
      a7: (__int64)v10,
      a8: (__int64)v9);
    sub_140833970(a1: v10);
    sub_140833970(a1: v11);
    sub_140833970(a1: v9);
    v3 = (void (__fastcall ***)(_QWORD, __int64))v5;
    if ( v5 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
      (**v3)(a1: v3, a2: 1);
  }
  sub_140808B00(a1: &v6);
  return 1;
}
