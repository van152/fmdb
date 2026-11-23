__int64 __fastcall sub_141524360(__int64 a1)
{
  int v1; // r8d
  __int64 result; // rax
  __int64 v3; // [rsp+28h] [rbp-30h] BYREF
  int v4; // [rsp+30h] [rbp-28h]
  unsigned __int64 v5; // [rsp+34h] [rbp-24h]
  __int64 v6; // [rsp+3Ch] [rbp-1Ch]
  int v7; // [rsp+44h] [rbp-14h]
  __int64 v8; // [rsp+48h] [rbp-10h]
  __int16 v9; // [rsp+50h] [rbp-8h]

  v1 = *(_DWORD *)(a1 + 40);
  result = 0;
  switch ( v1 )
  {
    case 10:
    case 11:
    case 12:
    case 13:
    case 14:
    case 25:
    case 27:
    case 40:
    case 64:
    case 65:
    case 70:
    case 82:
    case 83:
      v3 = 0;
      v4 = v1;
      v5 = 0xFFFFFFFF00000000uLL;
      v6 = 0;
      v7 = -1;
      v8 = 0x76C0001076C0001LL;
      v9 = 511;
      result = sub_141196230(*(_QWORD *)a1, &v3);
      break;
    default:
      return result;
  }
  return result;
}
