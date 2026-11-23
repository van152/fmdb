// THUNK ALIAS -> sub_14420EFB0 (jmp:0x141336010->0x14420efb0)
__int64 __fastcall sub_14420EFB0(__int64 a1, __int64 a2)
{
  __int64 v3; // rdx

  *(_QWORD *)a1 = 0x141759DF8LL;
  *(_BYTE *)(a1 + 8) = 13;
  LOBYTE(a2) = 13;
  sub_1412EA280(a1 + 16, a2);
  LOBYTE(v3) = 13;
  sub_1412EB230(a1 + 32, v3);
  *(_QWORD *)a1 = 0x14189EA48LL;
  *(_QWORD *)(a1 + 16) = 0x14189EB28LL;
  *(_QWORD *)(a1 + 32) = 0x14189EB48LL;
  return a1;
}
